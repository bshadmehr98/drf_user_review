import pytest
from django.contrib.auth.models import User
from django.utils import timezone
from blog.models import BlogPost, UserReview


@pytest.mark.django_db
def test_blogpost_model():
    title = "Test Blog Post"
    content = "This is a test blog post."
    published_date = timezone.now()

    blog_post = BlogPost.objects.create(
        title=title,
        content=content,
        created_at=published_date,
        updated_at=published_date
    )

    assert blog_post.id
    assert blog_post.title == title
    assert blog_post.content == content
    assert blog_post.created_at is not None
    assert blog_post.updated_at is not None


@pytest.mark.django_db
def test_blogpost_review_count_and_avg():
    user = User.objects.create(username='test_user', password='test_password')

    blog_post = BlogPost.objects.create(title="Test Post", content="Test Content")

    UserReview.objects.create(post=blog_post, user=user, rating=4)
    UserReview.objects.create(post=blog_post, user=user, rating=5)

    assert blog_post.review_count == 2
    assert blog_post.review_avg == 4.5
