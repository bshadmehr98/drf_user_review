from rest_framework import serializers
from blog.models import BlogPost, UserReview


class UserReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserReview
        exclude = ['post', 'user']

class BlogPostSerializer(serializers.ModelSerializer):
    review_count = serializers.ReadOnlyField()
    review_avg = serializers.ReadOnlyField()

    class Meta:
        model = BlogPost
        fields = '__all__'

