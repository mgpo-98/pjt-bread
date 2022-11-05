from django.urls import path
from . import views

app_name = 'bakeries'
urlpatterns = [
    # 지역별 빵집 목록 조회
    path('shops/region/<str:region_name>/', views.shops_by_region, name='shops_by_region'),
    # 빵 종류별 빵집 목록 조회
    path('shops/bread/<str:bread_name>/', views.shops_by_bread, name='shops_by_bread'),
    # 특정 빵집의 홈 상세 정보 조회
    path('shop/<int:shop_id>/', views.shop_home, name='shop_home'),
    # 빵집 탐색(search) 기능
    path('search/', views.search, name='search'),
]
