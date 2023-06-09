from rest_framework import permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Comment, Note, Photo, PhotoPage, PlanPage, Stamp
from .serializers import PlanSerializer


# 노트 조회 및 생성
class NoteView(APIView):
    pass


# 페이지 전체 조회 및 생성 -> 생성시 카테 고리를 보고 나눠 주세요~
class PageView(APIView):
    pass


# 사진첩 페이지
class DetailPhotoPageView(APIView):
    pass


# 댓글
class CommentView(APIView):
    pass


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
