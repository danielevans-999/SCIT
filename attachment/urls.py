from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
       ## authentication paths
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('logbook/', update_logbook, name = 'update_logbook'),
    path('uploads/', uploads, name='uploads'),
    path('summary/', weekly_summary, name = 'summary'),
    path('edit-logbook/<int:id>/', edit_logbook, name='edit_logbook'),
    path('student-registration/', student_registration, name = 'student_registration')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)