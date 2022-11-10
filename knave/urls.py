from django.urls import path
from . import views

app_name = 'knave'

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('channel/<str:id>', views.channel, name='channel'),
    # path('keyword/', views.keyword, name='keyword'),
    path('video/<str:id>', views.video, name='video'),
]
