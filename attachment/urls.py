from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
       ## authentication paths
    path('register/', register, name='register'),
    path('student-login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    ## Student URL's
    path('logbook/', update_logbook, name = 'update_logbook'),
    path('uploads/', uploads, name='uploads'),
    path('summary/', weekly_summary, name = 'summary'),
    path('edit-logbook/<int:id>/', edit_logbook, name='edit_logbook'),
    path('delete_log/', delete_logbook, name = 'delete_log' ),
    path('student-registration/', student_registration, name = 'student_registration'),
    path('linkedin-internships/', internships, name = 'internships'),
    path('request-supervision/', request_supervision, name =  'request_supervision' ),

    ## Organisation Supervisor URL's
    path('staff-login/', staff_login, name='staff-login'),
    path('staff-logout/', staff_logout, name='staff-logout'),
    path('organisation-assessment/', orgs_supevisor_assessment,  name='orgs_supevisor_assessment' ),
    path('process-assessment/<int:id>/', proc_assessment, name = 'proc_assessment'),
    path('org-logbook-assessment/<int:id>/', orgs_logbook_assessment, name = 'orgs_logbook_assessment'),
    path('internships/', students_internships, name='students_internships'),


    ## Admin URL's
    path('', admin_students, name = "admin_students"),
    path('assign-supervisor/', add_supervisor, name='add_supervisor'),
    path('scores/', view_scores, name = 'view_scores'),
    path('export_xls/<str:code>/', xls_export,  name = 'xls_export'), 
    path('post_internship/', post_internship, name='post_internship'),

    # Lectures's URL's
    path('lecturer-assessment/', lec_dashboard, name='lecturer_assessment'),
    path('process-lecturer-assessment/<int:id>/', proc_lec_assessment, name = 'proc_lec_assessment'),
    path('lecturer-view-logbooks/', view_logbook, name = 'view_logbook'),
    path('student-logbook-view/<int:id>/', proc_view_logbook, name = 'proc_view_logbook'),
    path('lecturer_view_reports/', view_report, name = 'view_report')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)