from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import User, Profile

# Register your models here
# .

class ProfileInLine(admin.StackedInline):
    model = Profile
    fields = ['avatar', 'gender', 'user_information', 'phone_number', 'following_count', 'followers_count']


class UserProfileAdmin(UserAdmin):
    inlines = [ProfileInLine]


# class ProfileInline(admin.StackedInline):
#     model = Profile
#     fields = ['birth_date', 'avatar']
#
#
# class UserProfileAdmin(UserAdmin):
#     inlines = [ProfileInline]

# admin.site.register(User, UserProfileAdmin)


admin.site.register(User, UserProfileAdmin)