from rest_framework import permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Comment, Note, PhotoPage, PlanPage, Stamp
from .serializers import (CommentSerializer, DetailNoteSerializer,
                          DetailPhotoPageSerializer, NoteSerializer,
                          PhotoPageSerializer, PlanSerializer)


# 노트 조회 및 생성
class NoteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, group_id):
        notes = Note.objects.filter(group_id=group_id).order_by("-created_at")
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk=None):
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DetailNoteView(APIView):
    def get(self, request, note_id):
        note = get_object_or_404(Note, id=note_id)
        serializer = DetailNoteSerializer(note)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, note_id):
        note = get_object_or_404(Note, id=note_id)
        serializer = NoteSerializer(note, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # pk = note_id
    def delete(self, request, note_id):
        note = get_object_or_404(Note, id=note_id)
        note.delete()
        return Response({"message": "노트가 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)


# 사진 페이지
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


# 사진 상세 페이지
class DetailPhotoPageView(APIView):
    def get(self, request, photo_id):
        photo = get_object_or_404(PhotoPage, id=photo_id)
        serializer = DetailPhotoPageSerializer(photo)
        return Response(serializer.data)

    # 댓글 저장
    def post(self, request, photo_id):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(photo_id=photo_id, user_id=request.user.id)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, photo_id):
        photo = get_object_or_404(PhotoPage, id=photo_id)
        serializer = DetailPhotoPageSerializer(photo, data=request.data, partial=True)
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

    def put(self, request, comment_id):
        comment = get_object_or_404(Comment, user=request.user, id=comment_id)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, comment_id):
        # permission_classes = [permissions.IsAuthenticated]
        comment = get_object_or_404(Comment, user=request.user, id=comment_id)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PlanPageView(APIView):
    def get(self, request, note_id):
        plan = PlanPage.objects.filter(diary_id=note_id)
        serializer = PlanSerializer(plan, many=True)
        return Response(serializer.data)

    def post(self, request, note_id):
        serializer = PlanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(diary_id=note_id)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
