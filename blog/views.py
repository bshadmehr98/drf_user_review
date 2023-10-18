from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from blog.models import BlogPost, UserReview
from blog.serializers import BlogPostSerializer, UserReviewSerializer


class BlogPostListView(generics.ListAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticated]



class UserReviewCreateView(generics.CreateAPIView):
    serializer_class = UserReviewSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        post_id = self.kwargs.get('post_id')
        user = request.user
        self.kwargs["user"] = user
        

        # Retrieve the associated blog post
        post = get_object_or_404(BlogPost, pk=post_id)

        existing_review = UserReview.objects.filter(post_id=post_id, user=user).first()
        
        if existing_review:
            # Update the existing review
            final_status = status.HTTP_200_OK
            serializer = self.get_serializer(existing_review, data=request.data)
        else:
            # Create a new review
            data = request.data.copy()
            data['post'] = post_id  # Add the post_id to the data
            final_status = status.HTTP_201_CREATED
            serializer = self.get_serializer(data=data)
        
        serializer.is_valid(raise_exception=True)
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=final_status, headers=headers)
        

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(BlogPost, pk=post_id)
        serializer.save(post=post, user=self.kwargs.get('user'))