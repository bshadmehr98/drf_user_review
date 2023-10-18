import json
from django.urls import reverse
from rest_framework import status
from blog.models import BlogPost, UserReview
from blog.serializers import BlogPostSerializer, UserReviewSerializer
import pytest
from django.contrib.auth.models import User

@pytest.fixture
def user2(db):
    return User.objects.create_user(username='testuser', password='testpassword')

@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser2', password='testpassword')

@pytest.fixture
def blog_post(db):
    return BlogPost.objects.create(title='Test Post', content='Test Content')

@pytest.fixture
def existing_review(db, blog_post, user):
    return UserReview.objects.create(post=blog_post, user=user, rating=3)

def test_blogpost_list_view(client, blog_post, user):
    url = reverse('blogpost-list')
    client.force_login(user)

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    expected_data = BlogPostSerializer([blog_post], many=True).data
    assert response.json() == expected_data

def test_userreview_create_view(client, blog_post, user2):
    url = reverse('userreview-create', kwargs={'post_id': blog_post.id})
    review_data = {'rating': 4}
    client.force_login(user2)

    response = client.post(url, review_data, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    expected_data = UserReviewSerializer(UserReview.objects.first()).data
    assert response.json() == expected_data

def test_userreview_create_view_existing_review(client, blog_post, existing_review, user):
    url = reverse('userreview-create', kwargs={'post_id': blog_post.id})
    review_data = {'rating': 4}
    client.force_login(user)

    response = client.post(url, review_data, format='json')

    assert response.status_code == status.HTTP_200_OK

    updated_review = UserReview.objects.get(pk=existing_review.pk)
    assert updated_review.rating == 4
