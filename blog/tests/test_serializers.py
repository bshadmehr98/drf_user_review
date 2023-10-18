import pytest
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
from blog.models import BlogPost, UserReview
from blog.serializers import UserReviewSerializer, BlogPostSerializer

@pytest.fixture
def blog_post():
    return BlogPost.objects.create(title='Test Blog Post', content='This is a test blog post.')

@pytest.fixture
def user(blog_post):
    return User.objects.create(username='test_user', password='test_password')

@pytest.fixture
def user_review(blog_post, user):
    return UserReview.objects.create(rating=4, post=blog_post, user=user)

@pytest.fixture
def invalid_user_review_data():
    return {'rating': 6, 'comment': 'Invalid rating!'}

@pytest.fixture
def invalid_blog_post_data():
    return {'title': 'Test Blog Post', 'content222': 'This is a test blog post.'}


@pytest.mark.django_db
def test_userreview_serializer(user_review, invalid_user_review_data):
    valid_data = {
        'rating': 4,
    }
    user_review_serializer = UserReviewSerializer(instance=user_review, data=valid_data)
    assert user_review_serializer.is_valid()

    with pytest.raises(ValidationError):
        UserReviewSerializer(instance=user_review, data=invalid_user_review_data).is_valid(raise_exception=True)

@pytest.mark.django_db
def test_blogpost_serializer(blog_post, invalid_blog_post_data):
    valid_data = {
        'title': 'Test Blog Post',
        'content': 'This is a test blog post.',
        'rating': 5,
    }
    blog_post_serializer = BlogPostSerializer(instance=blog_post, data=valid_data)
    assert blog_post_serializer.is_valid()

    # Invalid BlogPost data
    with pytest.raises(ValidationError):
        BlogPostSerializer(instance=blog_post, data=invalid_blog_post_data).is_valid(raise_exception=True)