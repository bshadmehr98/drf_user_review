from django.contrib import admin
from blog.models import BlogPost, UserReview

# Register your models here.
class UserReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'rating']
    list_filter = ['post', 'rating']
    search_fields = ['user__username']

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'content', 'review_count', 'review_avg']
    search_fields = ['title', 'content']
    readonly_fields = ['review_count', 'review_avg']

    def review_count(self, obj):
        return obj.review_count

    def review_avg(self, obj):
        return obj.review_avg

    review_count.short_description = 'Review Count'
    review_avg.short_description = 'Review Average'
    
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(UserReview, UserReviewAdmin)