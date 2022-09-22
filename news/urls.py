from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .views import NewsViewSet, StatusViewSet

router = DefaultRouter()
router.register('news', NewsViewSet, basename='news')
router.register('statuses', StatusViewSet, basename='statuses')


urlpatterns = [
    path('', include(router.urls)),
    path('news/<int:news_id>/', views.NewsUpdateDestroyAPIView.as_view()),
    path('news/<int:news_id>/comments/', views.CommentListCreateAPIView.as_view()),
    path('news/<int:news_id>/comments/<int:pk>/', views.CommentRetrieveDestroyUpdateAPIView.as_view()),
    path('news/<int:news_id>/<str:status_slug>/', views.NewsStatusView.as_view()),
    path('news/<int:news_id>/comments/<int:comment_id>/<str:status_slug>/', views.CommentStatusView.as_view()),
]