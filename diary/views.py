from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from diary.models import Note
from diary.serializers import NoteCreateSerializer, NoteSerializer


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
class PageView(APIView):
    pass


class DetailPhotoPageView(APIView):
    pass


class CommentView(APIView):
    pass


class DetailPlanPageView(APIView):
    pass


class Trash(APIView):
    pass


class Stamp(APIView):
    pass
