from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
# Create your models here.


class User(AbstractUser):
    pass


class Profile(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        related_name='profile',
        on_delete=models.CASCADE,
        verbose_name='User'
    )

    avatar = models.ImageField(null=False, blank=False, upload_to='avatars', verbose_name='Avatar')
    user_information = models.TextField(null=True, blank=True, verbose_name='Tell about yourself')
    phone_number = models.CharField(max_length=12, null=True, blank=True, verbose_name='Phone Number')

    GENDER_CHOICE = (
        ('M', 'Male'),
        ('F', 'Female')
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICE, null=True, blank=True, verbose_name='Gender')
    post_count = models.PositiveIntegerField(default=0)
    following_count = models.PositiveIntegerField(default=0)
    followers_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.username + "'s Profile"

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
