from django.urls import path
from . import views

app_name = 'knave'

urlpatterns = [
    # 메인 화면
    path('', views.index, name='index'),
    # 프론트엔드 샌드박스
    path('test/', views.test, name='test'),
    # 기본 검색 쿼리 수신
    path('search/', views.search, name='search'),
    # 채널 내 영상(10개) 검색
    path('channel/<str:id>', views.channel, name='channel'),
    # path('keyword/', views.keyword, name='keyword'),
    # 키워드 영상(10개) 검색
    path('video/<str:id>', views.video, name='video'),
    # path('analysis/<str:id>', views.one_analysis, name='analysis'),
    # 키워드 영상(10개) 검색
    path('analysus/', views.list_analysis, name='analysus'),
    # 에러페이지 기본 연결 및 리디렉션
    path('error/', views.error, name='error'),
]
