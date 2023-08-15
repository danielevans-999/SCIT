from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
       ## authentication paths
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logbook/', update_logbook, name = 'update_logbook'),
    path('summary/', weekly_summary, name = 'summary')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)