from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from instagram.models import Publication
from .serializers import PublicationSerializer, IsOwnerOrReadOnly, IsAuthenticatedAndOwnerOrReadOnly

# Create your views here.


class PublicationViewsSet(ModelViewSet):
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'
    lookup_url_kwarg = 'id'

    def get_likes_count(self, publication):
        return publication.user_likes.count()

    @action(detail=True, methods=['post'])
    def like(self, request, id=None):
        publication = self.get_object()
        user = request.user
        if user in publication.user_likes.all():
            return JsonResponse({'detail': 'You have already liked this publication'}, status=400)
        publication.user_likes.add(user)
        publication.likes += 1
        publication.save()
        likes_count = self.get_likes_count(publication)
        return JsonResponse({'likes_count': likes_count})

    @action(detail=True, methods=['delete'])
    def unlike(self, request, id=None):
        publication = self.get_object()
        user = request.user
        if user in publication.user_likes.all():
            publication.user_likes.remove(user)
            publication.likes -= 1
            publication.save()
            likes_count = self.get_likes_count(publication)
            return JsonResponse({'likes_count': likes_count})
        else:
            return JsonResponse({'detail': 'You have not liked this publication'}, status=400)
