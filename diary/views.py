import os

import tabulate
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.mail import send_mail
from rest_framework import permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from diary import destinations as de
from user.models import UserGroup
from user.serializers import GroupSerializer

from .models import Comment, Note, PhotoPage, PlanPage, Stamp
from .serializers import (
    CommentSerializer,
    DetailNoteSerializer,
    DetailPhotoPageSerializer,
    MarkerSerializer,
    NoteSerializer,
    PhotoPageSerializer,
    PlanSerializer,
    StampSerializer,
)


# 노트 조회 및 생성
class NoteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, group_id):
        notes = Note.objects.filter(group_id=group_id, status="0").order_by(
            "-created_at"
        )
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, group_id=None):
        serializer = NoteSerializer(data=request.data)
        print(request.user)
        if serializer.is_valid():
            # 같은 그룹 같은 노트 작성 불가
            if Note.objects.filter(
                name=serializer.validated_data.get("name"),
                group_id=serializer.validated_data.get("group"),
            ).exists():
                error_message = {"error": "이미 같은 이름의 노트가 존재합니다."}
                return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DetailNoteView(APIView):
    def get(self, request, note_id):
        note = get_object_or_404(Note, id=note_id, status="0")
        serializer = DetailNoteSerializer(note)
        group_exists = UserGroup.objects.filter(
            id=serializer.data["group"], members=request.user
        ).exists()
        if not group_exists:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, note_id):
        note = get_object_or_404(Note, id=note_id)
        serializer = NoteSerializer(note, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, note_id):
        note = get_object_or_404(Note, id=note_id)
        delete_note = NoteSerializer(note).data
        delete_note["status"] = 3
        serializer = NoteSerializer(note, data=delete_note, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 사진 페이지
class PhotoPageView(APIView):
    def get(self, request, note_id, offset=0):
        limit = 6
        photos = PhotoPage.objects.filter(diary_id=note_id, status="0")[
            offset : offset + limit
        ]
        serializer = PhotoPageSerializer(photos, many=True)
        return Response(serializer.data)

    def post(self, request, note_id):
        serializer = PhotoPageSerializer(data=request.data)
        if serializer.is_valid():
            note = get_object_or_404(Note, id=note_id)
            serializer.save(diary=note)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 사진 상세 페이지
class DetailPhotoPageView(APIView):
    def get(self, request, photo_id):
        photo = get_object_or_404(PhotoPage, id=photo_id, status="0")
        serializer = DetailPhotoPageSerializer(photo)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 댓글 저장
    def post(self, request, photo_id):
        serializer = CommentSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save(photo_id=photo_id, user_id=request.user.id)
            return Response(serializer.data, status=status.HTTP_200_OK)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 부분 수정이 유리하게 수정
    def patch(self, request, photo_id):
        photo = get_object_or_404(PhotoPage, id=photo_id)
        serializer = DetailPhotoPageSerializer(photo, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, photo_id):
        photo = get_object_or_404(PhotoPage, id=photo_id, status__in=[0, 1])
        delete_photo = DetailPhotoPageSerializer(photo).data
        delete_photo["status"] = 3

        image_file_path = photo.image.path
        image_file_name = os.path.basename(image_file_path)

        with open(image_file_path, "rb") as f:
            image_data = f.read()

        delete_photo["image"] = SimpleUploadedFile(image_file_name, image_data)

        serializer = PhotoPageSerializer(photo, data=delete_photo, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


# 댓글
class CommentView(APIView):
    def get(self, request, photo_id, comment_id):
        comment = get_object_or_404(
            Comment, user=request.user, id=comment_id, status__in=[0, 1]
        )
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, comment_id):
        comment = get_object_or_404(
            Comment, user=request.user, id=comment_id, status__in=[0, 1]
        )

        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, comment_id):
        comment = get_object_or_404(
            Comment, user=request.user, id=comment_id, status__in=[0, 1]
        )
        delete_comment = CommentSerializer(comment).data
        delete_comment["status"] = 3
        serializer = CommentSerializer(comment, data=delete_comment, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PlanPageView(APIView):
    def get(self, request, note_id):
        plan = PlanPage.objects.filter(diary_id=note_id, status="0")
        serializer = PlanSerializer(plan, many=True)
        return Response(serializer.data)

    def post(self, request, note_id):
        for plan in request.data["plan_set"]:
            serializer = PlanSerializer(data=plan)
            if serializer.is_valid():
                serializer.save(diary_id=note_id)
        return Response(status=status.HTTP_200_OK)

    # 전체 삭제
    def delete(self, request, note_id):
        plan_set = PlanPage.objects.filter(diary_id=note_id, status__in=[0, 1])
        serializer_set = PlanSerializer(plan_set, many=True)
        for delete_plan in serializer_set.data:
            delete_plan["status"] = 3
            plan = get_object_or_404(PlanPage, id=delete_plan["id"])
            serializer = PlanSerializer(plan, data=delete_plan, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 계획표 페이지
class DetailPlanPageView(APIView):
    def get(self, request, plan_id):
        plan = get_object_or_404(PlanPage, id=plan_id, status="0")
        serializer = PlanSerializer(plan)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, plan_id):
        plan = get_object_or_404(PlanPage, id=plan_id, status__in=[0, 1])
        serializer = PlanSerializer(plan, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, plan_id):
        plan = get_object_or_404(PlanPage, id=plan_id, status__in=[0, 1])
        delete_plan = PlanSerializer(plan).data
        delete_plan["status"] = 3

        serializer = PlanSerializer(plan, data=delete_plan, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 휴지통
class Trash(APIView):
    def get(self, request):
        group = UserGroup.objects.filter(master_id=request.user.id, status=1)
        note = Note.objects.filter(
            group__members=request.user, group__status=0, status=1
        )
        note_ids = Note.objects.filter(group__members=request.user).values_list(
            "id", flat=True
        )
        photo = PhotoPage.objects.filter(
            diary_id__in=note_ids, diary__group__status=0, diary__status=0, status=1
        )
        noteserializer = NoteSerializer(note, many=True)
        photoserializer = PhotoPageSerializer(photo, many=True)
        groupserializer = GroupSerializer(group, many=True)
        data = {
            "note": noteserializer.data,
            "photo": photoserializer.data,
            "group": groupserializer.data,
        }
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        if "group_set" in request.data:
            group_set = request.data.get("group_set", [])
            updated_groups = []

            for group_data in group_set:
                group_id = group_data.get("id")
                group = get_object_or_404(UserGroup, id=group_id)
                group_serializer = GroupSerializer(group, data=group_data)

                if group_serializer.is_valid():
                    if group.status == "0":
                        group.status = "1"
                        status_code = status.HTTP_202_ACCEPTED

                    elif group.status == "1":
                        group.status = "0"
                        status_code = status.HTTP_200_OK

                    group_serializer.save()
                    updated_groups.append(group_serializer.data)

                else:
                    return Response(
                        group_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )

            return Response(updated_groups, status=status_code)

        elif "note_set" in request.data:
            note_set = request.data.get("note_set", [])
            updated_notes = []

            for note_data in note_set:
                note_id = note_data.get("id")
                note = get_object_or_404(Note, id=note_id)
                note_serializer = NoteSerializer(note, data=note_data)

                if note_serializer.is_valid():
                    if note.status == "0":
                        note.status = "1"
                        status_code = status.HTTP_202_ACCEPTED

                    elif note.status == "1":
                        note.status = "0"
                        status_code = status.HTTP_200_OK

                    note_serializer.save()
                    updated_notes.append(note_serializer.data)

                else:
                    return Response(
                        note_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )

            return Response(updated_notes, status=status_code)

        else:
            photo_set = request.data.get("photo_set", [])
            updated_photos = []

            for photo_data in photo_set:
                photo_id = photo_data.get("id")
                photo = get_object_or_404(PhotoPage, id=photo_id)
                photo_serializer = PhotoPageSerializer(photo, data=photo_data)

                if photo_serializer.is_valid():
                    if photo.status == "0":
                        photo.status = "1"
                        status_code = status.HTTP_202_ACCEPTED

                    elif photo.status == "1":
                        photo.status = "0"
                        status_code = status.HTTP_200_OK

                    photo_serializer.save()
                    updated_photos.append(photo_serializer.data)

                else:
                    return Response(
                        photo_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )

            return Response(updated_photos, status=status_code)


# 스탬프
class StampView(APIView):
    def post(self, request, photo_id):
        try:
            stamp = Stamp.objects.get(photo_id=photo_id)
            serializer = StampSerializer(stamp, data=request.data)

        except Stamp.DoesNotExist:
            serializer = StampSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(photo_id=photo_id, user_id=request.user.id)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            if stamp.status == "0":
                stamp.status = "1"
                serializer.save(photo_id=photo_id, user_id=request.user.id)
                return Response(serializer.data, status=status.HTTP_200_OK)
            elif stamp.status == "1":
                stamp.status = "0"
                serializer.save(photo_id=photo_id, user_id=request.user.id)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MarkerStampsView(APIView):
    def get(self, request, photo_location):
        user = request.user
        stamps = Stamp.objects.filter(
            user=user, photo__location=photo_location, photo__status=0, status=0
        )
        serializer = MarkerSerializer(stamps, many=True)
        return Response(serializer.data)


class SearchDestination(APIView):
    def post(self, request):
        test = de.search(request.data["destinations"])
        return Response(test, status=status.HTTP_200_OK)


class EmailView(APIView):
    def post(self, request, note_id):
        note = get_object_or_404(Note, id=note_id)
        serializer = DetailNoteSerializer(note)
        plan_set = serializer.data["plan_set"]
        note_name = serializer.data["name"]

        filtered_data = []  # 필터링된 데이터를 저장할 리스트

        for item in plan_set:
            filtered_item = {
                "title": item["title"],
                "start": item["start"],
                "location": item["location"],
            }
            filtered_data.append(filtered_item)

        formatted_data = ""

        for index, item in enumerate(filtered_data, start=1):
            formatted_data += f"{index}. 장소명: {item['title']}, 날짜: {item['start']}, 위치: {item['location']}\n"

        print(formatted_data)

        subject = f"{note_name}의 일정 안내"
        message = f"아래는 일정에 대한 정보입니다:\n\n{formatted_data}"

        recipient_list = request.data["members"]
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,  # Gmail 계정 이메일 주소
            recipient_list,
            fail_silently=False,
        )

        # 이메일 전송 후 리다이렉트 또는 응답 등을 처리
        return Response("이메일이 전송되었습니다.", status=status.HTTP_200_OK)
