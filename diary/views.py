from rest_framework.generics import get_object_or_404, get_object
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import permissions, status
from .models import Comment, Note, Photo, PhotoPage, PlanPage, Stamp
from .serializers import PhotoPageSerializer, DetailPhotoPageSerializer, CommentSerializer, PlanSerializer


# 노트 조회 및 생성
class NoteView(APIView):
        
    pass


# 노트 조회 및 생성

# 페이지 전체 조회 및 생성 -> 생성시 카테 고리를 보고 나눠 주세요~

class PageView(APIView):
    
    pass



class PhotoPageView(APIView):
    def get(self, request):
        photos = PhotoPage.objects.all()
        serializer = PhotoPageSerializer(photos, many=True)
        return Response(serializer.data)
        
    def post(self, request):
        serializer = PhotoPageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 사진첩 페이지
class DetailPhotoPageView(APIView):
    def get(self, request, photo_id):
        photo = get_object_or_404(PhotoPage, id=photo_id)
        serializer = DetailPhotoPageSerializer(photo)
        return Response(serializer.data)

    def put(self, request, photo_id):
        photo = get_object(PhotoPage, id=photo_id)
        serializer = DetailPhotoPageSerializer(photo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, photo_id):
        photo = get_object(request, id=photo_id)
        photo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 댓글
class CommentView(APIView):
    def get(self, request, comment_id):
        comment = get_object_or_404(Comment, user=request.user, id = comment_id)
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, comment_id):
        comment = get_object_or_404(Comment, user=request.user, id = comment_id)
        serializer = CommentSerializer(comment)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, review_id):
        # permission_classes = [permissions.IsAuthenticated]
        comment = get_object_or_404(Comment, user=request.user, id=review_id)
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
