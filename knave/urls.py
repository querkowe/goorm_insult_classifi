from django.urls import path
from . import views

app_name = 'knave'

urlpatterns = [
    path('', views.index, name='index'),
    path('test/', views.test, name='test'),
    path('search/', views.search, name='search'),
    path('channel/<str:id>', views.channel, name='channel'),
    # path('keyword/', views.keyword, name='keyword'),
    path('video/<str:id>', views.video, name='video'),
    # path('analysis/<str:id>', views.one_analysis, name='analysis'),
    path('analysus/', views.list_analysis, name='analysus'),
    path('error/', views.error, name='error'),
]
