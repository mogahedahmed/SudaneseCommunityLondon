from django.urls import path, include
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('vote/', include('vote.urls')),
    path('news/', include('news.urls')),
    path('contact/', include('contact.urls')),
    path('activities/', include('activities.urls')),
    path('regulations/', include('regulations.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
