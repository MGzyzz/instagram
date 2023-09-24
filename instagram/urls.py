from django.urls import path
from instagram import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('<int:id>/detail', views.PublicationUserDetail.as_view(), name='detail_publication'),
    path('<int:id>/create_comment', views.UploadComments.as_view(), name='create-comments'),
    path('create_publication', views.CreatePublication.as_view(), name='create-publication'),
    # path('<int:id>/like', views.Like.as_view(), name='like'),
    path('<int:id>/subscribe', views.Subscribe.as_view(), name='subscribe')
]