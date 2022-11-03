from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.conf import settings

# Create your models here.
class Review(models.Model):
    shop_id = models.CharField(max_length=20)
    content = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    visited_at = models.DateField('최근 방문일', null=True)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_articles')
    image = ProcessedImageField(upload_to='images/', blank=True,
                            processors=[ResizeToFill(1200, 960)],
                            format='JPEG',
                            options={'quality': 80})

class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()    
