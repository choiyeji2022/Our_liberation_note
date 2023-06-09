from rest_framework import permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Comment, Note, PhotoPage, PlanPage, Stamp
from .serializers import (CommentSerializer, DetailPhotoPageSerializer,
                          NoteCreateSerializer, NoteSerializer,
                          PhotoPageSerializer, PlanSerializer)


# 노트 조회 및 생성
class NoteView(APIView):
    def get(self, request):
        notes = Note.objects.all().order_by("-created_at")
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = NoteCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(group_id=request.group.id)
            return Response(
                serializer.data, {"message": "노트생성 완료!"}, status=status.HTTP_201_CREATED
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, note_id):
        note = get_object_or_404(Note, id=note_id)
        serializer = NoteCreateSerializer(note, data=request.data)
        if serializer.valid():
            serializer.save()
            return Response(
                serializer.data, {"message": "노트 수정 완료!"}, status=status.HTTP_200_OK
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, note_id):
        note = get_object_or_404(Note, id=note_id)
        note.delete()
        return Response({"message": "노트가 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)


# 노트 조회 및 생성

# 페이지 전체 조회 및 생성 -> 생성시 카테 고리를 보고 나눠 주세요~


class PageView(APIView):
    pass


class PhotoPageView(APIView):
    def get(self, request, note_id):
        photos = PhotoPage.objects.filter(diary_id=note_id)
        serializer = PhotoPageSerializer(photos, many=True)
        return Response(serializer.data)

    def post(self, request, note_id):
        serializer = PhotoPageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(diary_id=note_id)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 사진상세 페이지
class DetailPhotoPageView(APIView):
    def get(self, request, photo_id):
        photo = get_object_or_404(PhotoPage, id=photo_id)
        serializer = DetailPhotoPageSerializer(photo)
        return Response(serializer.data)
    
    def post(self, request, photo_id):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(photo_id=photo_id, user_id=request.user.id)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #부분 수정이 유리하게 수정
    def patch(self, request, photo_id):
        photo = get_object_or_404(PhotoPage, id=photo_id)
        serializer = DetailPhotoPageSerializer(photo, data=request.data, partail=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, photo_id):
        photo = get_object_or_404(request, id=photo_id)
        photo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 댓글
class CommentView(APIView):
    def get(self, request, comment_id):
        comment = get_object_or_404(Comment, user=request.user, id=comment_id)
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, comment_id):
        comment = get_object_or_404(Comment, user=request.user, id=comment_id)
        serializer = CommentSerializer(comment)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, comment_id):
        # permission_classes = [permissions.IsAuthenticated]
        comment = get_object_or_404(Comment, user=request.user, id=comment_id)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 계획표 페이지
class DetailPlanPageView(APIView):
    def get(self, request, plan_id):
        plan = get_object_or_404(PlanPage, id=plan_id)
        serializer = PlanSerializer(plan)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, plan_id):
        plan = get_object_or_404(PlanPage, id=plan_id)
        serializer = PlanSerializer(plan, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, plan_id):
        plan = get_object_or_404(PlanPage, id=plan_id)
        plan.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TodoView(APIView):
    pass


# 휴지통
class Trash(APIView):
    pass


# 스템프
class StampView(APIView):
    pass
