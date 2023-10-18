from django.urls import path
from blog.views import BlogPostListView, UserReviewCreateView

urlpatterns = [
    path('posts/', BlogPostListView.as_view(), name='blogpost-list'),
    path('reviews/create/<int:post_id>/', UserReviewCreateView.as_view(), name='userreview-create'),
]