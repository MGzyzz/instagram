from django.db import models
from django.contrib.auth import get_user_model
from .publication import Publication


class Comment(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(max_length=100, verbose_name='Text comments')
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'Comment by {self.user.username}, on Publication {self.publication.id}'