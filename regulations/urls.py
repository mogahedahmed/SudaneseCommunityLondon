from django.urls import path
from . import views

urlpatterns = [
    path('', views.regulation_list, name='regulations'),
    path('<int:pk>/', views.regulation_detail, name='regulation_detail'),
]
