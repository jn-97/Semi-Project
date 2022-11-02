from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill



# Create your models here.

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=40)
    content = models.TextField()
    RATING = [
        (1, "★"),
        (2, "★★"),
        (3, "★★★"),
        (4, "★★★★"),
        (5, "★★★★★"),
    ]

    grade = models.IntegerField(choices=RATING, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = ProcessedImageField(
        upload_to = 'images/',
        blank = True,
        processors=[ResizeToFill(300, 400)],
        format='JPEG',
        options={"quality": 90},
    )
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="like_reviews"
    )
    # 조회수
    hits = models.IntegerField(default=0)

class Comment(models.Model):
    RATING = [
        (5, "★★★★★"),
        (4, "★★★★"),
        (3, "★★★"),
        (2, "★★"),
        (1, "★"),
    ]
    grade = models.IntegerField(choices=RATING, default=None)
    content = models.TextField(max_length=300, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


