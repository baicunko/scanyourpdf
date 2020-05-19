from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.upload, name='pdf-upload'),
    path('failed/',views.failed, name='pdf-fail'),
    path('home/', views.home, name='pdf-home'),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
