from django.db import models
from django.core.cache import cache
from django.contrib.auth.models import User

from UserReview.models import TimestampedModel
from django.core.validators import MinValueValidator, MaxValueValidator


class BlogPost(TimestampedModel):
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.title

    @property
    def review_count(self):
        cache_key = f'review_count_{self.pk}'
        count = cache.get(cache_key)
        if count is None:
            count = self.reviews.count()
            cache.set(cache_key, count, timeout=60)  # Cache for 1 minute
        return count

    @property
    def review_avg(self):
        cache_key = f'review_avg_{self.pk}'
        avg = cache.get(cache_key)
        print(f"Cache value({avg}) for key ({cache_key})")
        if avg is None:
            reviews = self.reviews.all()
            if reviews:
                total_rating = sum(review.rating for review in reviews)
                avg = total_rating / len(reviews)
            else:
                avg = 0.0
            cache.set(cache_key, avg, timeout=60)  # Cache for 1 minute
        return round(avg, 1)


class UserReview(TimestampedModel):
    post = models.ForeignKey(BlogPost, related_name='reviews', on_delete=models.CASCADE, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )

    def __str__(self):
        return f'{self.user.username}\'s Review for {self.post.title}'
