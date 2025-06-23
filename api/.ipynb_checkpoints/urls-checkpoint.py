from django.urls import path
from . import views
from .views import ArticleListAPIView, ArticleDetailAPIView


urlpatterns = [
    #path('', views.getData),
    path('articles/', ArticleListAPIView.as_view(), name='article-list'),
    path('articles/<slug:slug>/', ArticleDetailAPIView.as_view(), name='article-detail'),
]
