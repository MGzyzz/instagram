from django.contrib import admin
from instagram.models import Publication, Comment, Subscription

# Register your models here.
class PublicationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at']



admin.site.register(Publication, PublicationAdmin)
admin.site.register(Comment)
admin.site.register(Subscription)