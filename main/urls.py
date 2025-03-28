from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('vote/', include('vote.urls')),      # التصويت
    path('news/', include('news.urls')),      # الأخبار الديناميكية
    path('contact/', include('contact.urls')),
    path('activities/', include('activities.urls')),
    path('regulations/', include('regulations.urls')),
    path('contact/', include('contact.urls')),

]
