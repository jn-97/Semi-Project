from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill



# Create your models here.

class Restaurant(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    sorted = models.CharField(max_length=20)
    runtime = models.CharField(max_length=100)
    closing = models.CharField(max_length=100)
    region = models.CharField(max_length=20)
    introduce = models.CharField(max_length=1000)
    number = models.CharField(max_length=20)
    address = models.CharField(max_length=100)

    image1 = ProcessedImageField(
        upload_to = 'images/',
        blank = True,
        processors=[ResizeToFill(251, 251)],
        format='JPEG',
        options={"quality": 80},
    )
    image2 = ProcessedImageField(
        upload_to = 'images/',
        blank = True,
        processors=[ResizeToFill(251, 251)],
        format='JPEG',
        options={"quality": 80},
    )
    image3 = ProcessedImageField(
        upload_to = 'images/',
        blank = True,
        processors=[ResizeToFill(251, 251)],
        format='JPEG',
        options={"quality": 80},
    )
    image4 = ProcessedImageField(
        upload_to = 'images/',
        blank = True,
        processors=[ResizeToFill(251, 251)],
        format='JPEG',
        options={"quality": 80},
    )
    image5 = ProcessedImageField(
        upload_to = 'images/',
        blank = True,
        processors=[ResizeToFill(251, 251)],
        format='JPEG',
        options={"quality": 80},
    )
    hits = models.IntegerField(default=0)
    want_go = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="liked_user"
    )



class Comment(models.Model):
    RATING = [
        (1, "⭐️"),
        (2, "⭐️⭐️"),
        (3, "⭐️⭐️⭐️"),
        (4, "⭐️⭐️⭐️⭐️"),
        (5, "⭐️⭐️⭐️⭐️⭐️"),
    ]
    grade = models.IntegerField(choices=RATING, default=None)
    content = models.TextField(max_length=300, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
