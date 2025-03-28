from django.urls import path
from . import views

urlpatterns = [
    path('<str:category>/', views.news_list, name='news_by_category'),
    path('detail/<int:pk>/', views.news_detail, name='news_detail'),  # ← الرابط لتفاصيل الخبر
]
