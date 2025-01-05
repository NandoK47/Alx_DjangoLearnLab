from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Post, Like
from accounts.models import CustomUser
from notifications.models import Notification
from rest_framework.generics import get_object_or_404

# Create your views here.

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = 'PostPagination'
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'content']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class FeedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        following_users = request.user.following.all()
        posts = Post.objects.filter(author__in=following_users).order_by()
        data = [{"author": post.author.username, "title": post.title, "content": post.content, "created_at": post.created_at} for post in posts]
        return Response(data, 'status=status'.HTTP_200_OK)

class LikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            post = get_object_or_404(Post, pk=pk)
            like, created = Like.objects.get_or_create(user=request.user, post=post)

            if created:
                # Create a notification
                Notification.objects.create(
                    recipient=post.author,
                    actor=request.user,
                    verb="liked your post",
                    target=post
                )
                return Response({"message": "Post liked."}, status=status.HTTP_201_CREATED)
            else:
                return Response({"message": "Post already liked."}, status=status.HTTP_400_BAD_REQUEST)
        except Post.DoesNotExist:
            return Response({"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

class UnlikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            post = get_object_or_404(post, pk=pk)
            like = Like.objects.filter(user=request.user, post=post)

            if like.exists():
                like.delete()
                return Response({"message": "Post unliked."}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "You haven't liked this post."}, status=status.HTTP_400_BAD_REQUEST)
        except Post.DoesNotExist:
            return Response({"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)