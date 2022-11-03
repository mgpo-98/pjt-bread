from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('', views.index, name='index'), # 빵집 구분 없이 모든 리뷰

    # http://127.0.0.1:8000/reviews/<int:shop_pk>/create/ 리뷰 작성
    path('<int:shop_id>/create/', views.create, name='create'),

    # http://127.0.0.1:8000/reviews/<int:pk>/ 특정 리뷰 상세 조회
    path('<int:pk>/', views.detail, name='detail'), 

    # http://127.0.0.1:8000/reviews/<int:pk>/update/ 리뷰 수정
    path('<int:pk>/update/', views.update, name='update'),
    # http://127.0.0.1:8000/reviews/<int:pk>/delete/ 리뷰 삭제
    path('<int:pk>/delete', views.delete, name='delete'),
    # http://127.0.0.1:8000/reviews/<int:pk>/like/ 리뷰 좋아요
    path('<int:pk>/like/', views.like, name='like'),
    # http://127.0.0.1:8000/reviews/<int:pk>/comments/create/ 댓글 작성
    path('<int:pk>/comments/', views.comment_create, name='comment_create'),
    # http://127.0.0.1:8000/reviews/<int:pk>/comments/<int:comment_pk>/delete/ 댓글 삭제
    path('<int:pk>/comments/<int:comment_pk>/delete/', views.comment_delete, name ='comment_delete'),
]