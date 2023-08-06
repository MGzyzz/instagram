from django.db import models
from django.contrib.auth import get_user_model


class Subscription(models.Model):
    subscriber = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='subscription')
    followed_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.subscriber} subscribe {self.followed_user}'