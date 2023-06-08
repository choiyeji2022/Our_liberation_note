from django.shortcuts import get_object_or_404, get_object
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import PhotoPage, Comment
from .serializers import PhotoPageSerializer, DetailPhotoPageSerializer, CommentSerializer

# 노트 조회 및 생성
class NoteView(APIView):
        
    pass

# 노트 조회 및 생성
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


class DetailPlanPageView(APIView):
    pass


class Trash(APIView):
    pass


class Stamp(APIView):
    pass





