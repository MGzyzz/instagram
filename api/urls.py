from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from api import views


router = routers.DefaultRouter()
router.register(r'publication', views.PublicationViewsSet)

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
    path('publications/<int:id>/like/', views.PublicationViewsSet.as_view({'post': 'like'}), name='publication-like'),
    path('publications/<int:id>/unlike/', views.PublicationViewsSet.as_view({'delete': 'unlike'}), name='publication-unlike'),
    path('login/', obtain_auth_token, name='api_token_auth')
]