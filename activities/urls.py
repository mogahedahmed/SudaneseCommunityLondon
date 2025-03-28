from django.urls import path
from . import views

urlpatterns = [
    path('', views.activities_view, name='activities'),
    path('<int:pk>/', views.activity_detail_view, name='activity_detail'),
]
