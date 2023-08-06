from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

class Publication(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='publications')
    image = models.ImageField(upload_to='publications')
    description = models.TextField(max_length=250, verbose_name='Description')
    likes = models.IntegerField(default=0, verbose_name='Likes')
    comments_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    user_likes = models.ManyToManyField(get_user_model(), related_name='like_publications', blank=True)

    def __str__(self):
        return f'Publication by {self.user.username} - {self.created_at}'

    class Meta:
        ordering = ['-created_at']