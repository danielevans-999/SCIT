from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required,  user_passes_test
from django.http import JsonResponse
from datetime import timedelta
from datetime import datetime as mydate
from .forms import *
from .decorators import (prevent_login_access, prevent_admin_login_access)
from .emails import *
from .password_generator import generate_password
from linkedin_v2 import linkedin
from django.http import HttpResponse
import pandas as pd
from xlsxwriter import Workbook
from django.contrib import messages



# Student Views.

def register(request):
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    context = {'form': form}

    return render(request, 'attachment/register.html', context)

@prevent_login_access
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        allowed_domain = ['students.tukenya.ac.ke']
        if email.split('@')[1] not in allowed_domain:
            messages.error(request, 'Use your student email to login')
            return redirect('login')
        else:
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('summary')
            messages.error(request, 'incorrect credentials')
    return render(request, 'attachment/login.html')

@login_required
def update_logbook(request):
    start_date = request.user.student.start_date
    print(start_date)
    if request.method == 'POST':
        date = request.POST.get('date')
        description = request.POST.get('description')
        check_date =  mydate.strptime(date, '%Y-%m-%d').date()
        is_valid = (check_date >= start_date)
        if is_valid:
            LogBook.objects.create(
                date=date,
                description=description,
                student=request.user.student
            )
        return JsonResponse({'is_valid': is_valid})

    return render(request, 'attachment/update_logbook.html')

@login_required
def weekly_summary(request):
    print(request.user.email)
    if not request.user.updated_profile:
        return redirect('student_registration')
    
    current_user = request.user
    default_week = "week 1"
    logbooks = None
    student = Student.objects.get(user = current_user)
    start = student.start_date
    print(start + timedelta(days = 8))
     
    week = request.GET.get('week')
    if week == 'week 1':
        logbooks = LogBook.objects.filter(date__range=(start, start + timedelta(days = 6)), student = student).order_by('date')
        try:
            supervisor_comment = SupervisorComment.objects.get(student = student, week = 'week 1')
        except SupervisorComment.DoesNotExist:
            supervisor_comment = None
        print(logbooks)
        return render(request, 'attachment/summary.html', locals())
    
    elif week == 'week 2':
        logbooks =  LogBook.objects.filter(date__range=(start + timedelta(days = 6), start + timedelta(days = 13)), student = student).order_by('date')
        try:
            supervisor_comment = SupervisorComment.objects.get(student = student, week = 'week 2')
        except SupervisorComment.DoesNotExist:
            supervisor_comment = None
        return render(request, 'attachment/summary.html', locals())
    
    elif week == 'week 3':
        logbooks = LogBook.objects.filter(date__range=(start + timedelta(days = 13), start + timedelta(days = 20)), student = student).order_by('date')
        try:
            supervisor_comment = SupervisorComment.objects.get(student = student, week = 'week 3')
        except SupervisorComment.DoesNotExist:
            supervisor_comment = None
        return render(request, 'attachment/summary.html', locals())
    
    elif week == 'week 4':
        logbooks = LogBook.objects.filter(date__range=(start + timedelta(days = 22), start + timedelta(days = 29)), student = student).order_by('date')
        try:
            supervisor_comment = SupervisorComment.objects.get(student = student, week = 'week 4')
        except SupervisorComment.DoesNotExist:
            supervisor_comment = None
        print(logbooks)
        return render(request, 'attachment/summary.html', locals())
    
    elif week == 'week 5':
        logbooks = LogBook.objects.filter(date__range=(start + timedelta(days = 29), start + timedelta(days = 36)), student = student).order_by('date')
        try:
            supervisor_comment = SupervisorComment.objects.get(student = student, week = 'week 5')
        except SupervisorComment.DoesNotExist:
            supervisor_comment = None
        print(logbooks)
        return render(request, 'attachment/summary.html', locals())
    
    elif week == 'week 6':
        logbooks = LogBook.objects.filter(date__range=(start + timedelta(days = 36), start + timedelta(days = 43)), student = student).order_by('date')
        try:
            supervisor_comment = SupervisorComment.objects.get(student = student, week = 'week 6')
        except SupervisorComment.DoesNotExist:
            supervisor_comment = None
        print(logbooks)
        return render(request, 'attachment/summary.html', locals())
    
    elif week == 'week 7':
        logbooks = LogBook.objects.filter(date__range=(start + timedelta(days = 43), start + timedelta(days = 50)), student = student).order_by('date')
        try:
            supervisor_comment = SupervisorComment.objects.get(student = student, week = 'week 7')
        except SupervisorComment.DoesNotExist:
            supervisor_comment = None
        print(logbooks)
        return render(request, 'attachment/summary.html', locals())
    
    elif week == 'week 8':
        logbooks = LogBook.objects.filter(date__range=(start + timedelta(days = 50), start + timedelta(days = 57)), student = student).order_by('date')
        try:
            supervisor_comment = SupervisorComment.objects.get(student = student, week = 'week 8')
        except SupervisorComment.DoesNotExist:
            supervisor_comment = None
        print(logbooks)
        return render(request, 'attachment/summary.html', locals())
    
    elif week == 'week 9':
        logbooks = LogBook.objects.filter(date__range=(start + timedelta(days = 57), start + timedelta(days = 64)), student = student).order_by('date')
        try:
            supervisor_comment = SupervisorComment.objects.get(student = student, week = 'week 9')
        except SupervisorComment.DoesNotExist:
            supervisor_comment = None
        print(logbooks)
        return render(request, 'attachment/summary.html', locals())
    
    elif week == 'week 10':
        logbooks = LogBook.objects.filter(date__range=(start + timedelta(days = 64), start + timedelta(days = 71)), student = student).order_by('date')
        try:
            supervisor_comment = SupervisorComment.objects.get(student = student, week = 'week 10')
        except SupervisorComment.DoesNotExist:
            supervisor_comment = None
        print(logbooks)
        return render(request, 'attachment/summary.html', locals())
    
    elif week == 'week 11':
        logbooks =LogBook.objects.filter(date__range=(start + timedelta(days = 71), start + timedelta(days = 78)), student = student).order_by('date')
        try:
            supervisor_comment = SupervisorComment.objects.get(student = student, week = 'week 11')
        except SupervisorComment.DoesNotExist:
            supervisor_comment = None
        print(logbooks)
        return render(request, 'attachment/summary.html', locals())
    
    elif week == 'week 12':
        logbooks = LogBook.objects.filter(date__range=(start + timedelta(days = 78), start + timedelta(days = 85)), student = student).order_by('date')
        try:
            supervisor_comment = SupervisorComment.objects.get(student = student, week = 'week 12')
        except SupervisorComment.DoesNotExist:
            supervisor_comment = None
        print(logbooks)
        return render(request, 'attachment/summary.html', locals())
   
    logbooks = LogBook.objects.filter(date__range=(start, start + timedelta(days = 6)), student = student).order_by('date')
    try:
        supervisor_comment = SupervisorComment.objects.get(student = student, week = 'week 1')
    except SupervisorComment.DoesNotExist:
        supervisor_comment = None
    return render(request, 'attachment/summary.html', locals())

@login_required
def edit_logbook(request, id):
    logbook = get_object_or_404(LogBook, id = id)
    if request.method == 'POST':
        description = request.POST.get('update_desc')
        logbook.description = description
        logbook.save()
        return redirect('summary')
@login_required
def delete_logbook(request):
    id = request.GET.get('id')
    logbook = get_object_or_404(LogBook, id = id)
    logbook.delete()
    return redirect('summary')

        
@login_required
def student_registration(request):
    current_user = request.user
    status = current_user.updated_profile
    try:
        student = Student.objects.get(user = current_user)
    except Student.DoesNotExist:
        student = None
    print(student)
    if request.method == 'POST':
        name = request.POST.get('name')
        registration_number = request.POST.get('registration_number')
        course = request.POST.get('course')
        year = request.POST.get('year')
        department = request.POST.get('department')
        class_code = request.POST.get('class_code')
        organisation = request.POST.get('organisation')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        photo_url = request.FILES.get('pic')
        orgs_supervisor_email = request.POST.get('organisation_supervisor_email')
        orgs_supervisor_name = request.POST.get('organisation_supervisor_name')
        if not current_user.updated_profile:

            profile = Student.objects.create(

                name=name,
                registration_number=registration_number,
                course=course,
                year=year,
                department=department,
                class_code =class_code,
                organisation=organisation,
                start_date=start_date,
                end_date=end_date,
                user = current_user,
                photo_url = photo_url,

            )
            profile.user.is_student = True
            profile.user.updated_profile = True
            current_user.save()
            try:
                send_orgs_email(orgs_supervisor_email,orgs_supervisor_name, profile)
            except TimeoutError:
                return JsonResponse({'error': 'There is a network error.'})
            return redirect('summary')

    return render(request, 'attachment/student_registration.html', locals())

@login_required
def uploads(request):
    if not request.user.updated_profile:
        return redirect('student_registration')
    
    student = request.user.student
    if request.method == 'POST' and request.FILES.get('pdf_file'):
        pdf_file = request.FILES['pdf_file']
        uploaded_pdf = Reports.objects.create(student = student, pdf_file = pdf_file)
        uploaded_pdf.save()
    return render(request, "attachment/uploads.html")

def students_internships(request):
    internships = Internship.objects.all().order_by('-time_stamp')
    return render(request, 'attachment/internships_list.html', locals())
# def linkedin_auth(request):
#     api_key = '77jq3x3yj6br53'
#     api_secret = 'p9JQ1XyRazpZPYWg'
#     redirect_uri = 'http://127.0.0.1:8000/attachment/linkedin-internships/'
    
#     linkedin_auth_url = f"https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id={api_key}&redirect_uri={redirect_uri}&state=123456&scope=r_liteprofile,r_emailaddress,w_member_social"

#     return redirect(linkedin_auth_url)

    # token_url = "https://www.linkedin.com/oauth/v2/accessToken"
    # jobs_rl = "https://www.linkedin.com/v2/jobs"


    

def internships(request):
  return render(request, "attachment/internships.html", locals())
    
def logout_view(request):
    logout(request)
    return redirect('login')

## staff views

def staff_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        print(user)
        if user is not None and user.is_admin:
            login(request, user)
            print(user.is_admin)
            print(request.path)
            return redirect('add_supervisor')
        if user is not None and user.is_lecturer:
            login(request, user)
            return redirect('lecturer_assessment')
        if user is not None and user.is_supervisor:
            login(request, user)
            print(user is not None, 'Second Time')
            return redirect('orgs_supevisor_assessment')
    return render(request, 'attachment/staff_login.html')

@login_required(login_url='/attachment/staff-login/')
def orgs_supevisor_assessment(request):
    my_supervisor = OrganisationSupervisor.objects.get(user_id = request.user.id)
    students = my_supervisor.students.all()
    try:
        user_id = request.GET.get('id')
        print(user_id)
        student = User.objects.get(id = user_id).student
        scores = OrganisationAssessment.objects.get(student = student)
    except User.DoesNotExist:
        user_id = None
    except OrganisationAssessment.DoesNotExist:
        scores = None
    return render(request, 'attachment/organisation_dashboard.html',locals())

def proc_assessment(request, id):
    if request.method == 'POST':
        student = Student.objects.get(user_id = id)
        OrganisationAssessment.objects.create(
            punctuality = int(request.POST.get('panctuality')), 
            adherence_to_regulation = int(request.POST.get('regulations')), 
            workmanship = int(request.POST.get('workmanship')), 
            adaptability = int(request.POST.get('adaptability')), 
            communication = int( request.POST.get('communication')), 
            reliability = int(request.POST.get('reliability')),
            teamwork = int(request.POST.get('teamwork')), 
            general_remarks = request.POST.get('assessor_remarks'),
            student =student
            )
        student.assessed_by_employer = True
        student.save()
        return redirect('orgs_supevisor_assessment')

def orgs_logbook_assessment(request, id):
    student = Student.objects.get(user_id = id)
    default_week = "week 1"
    logbooks = None
    start = student.start_date
    week = request.GET.get('week')

    if request.method == 'POST':
        selected_week = request.POST.get('week')
        comment = request.POST.get('comment')
        comment_object = SupervisorComment.objects.create(week = selected_week, comment = comment, student = student)
        comment_object.status = True
        comment_object.save()
        return redirect('orgs_supevisor_assessment')
    
    if week == 'week 1':
        logbooks = LogBook.objects.filter(date__range=(start, start + timedelta(days = 8)), student = student).order_by('date')
        try:
            supervisor_comment = SupervisorComment.objects.get(student = student, week = 'week 1')
        except SupervisorComment.DoesNotExist:
            supervisor_comment = None
        print(logbooks)
        return render(request, 'attachment/supervisor_assessment.html', locals())
    elif week == 'week 2':
        logbooks =  LogBook.objects.filter(date__range=(start + timedelta(days = 8), start + timedelta(days = 15)), student = student).order_by('date')
        try:
            supervisor_comment = SupervisorComment.objects.get(student = student, week = 'week 2')
        except SupervisorComment.DoesNotExist:
            supervisor_comment = None
        print(logbooks)
        return render(request, 'attachment/supervisor_assessment.html', locals())
    
    elif week == 'week 3':
        logbooks = LogBook.objects.filter(date__range=(start + timedelta(days = 15), start + timedelta(days = 22)), student = student).order_by('date')
        try:
            supervisor_comment = SupervisorComment.objects.get(student = student, week = 'week 3')
        except SupervisorComment.DoesNotExist:
            supervisor_comment = None
        print(logbooks)
        return render(request, 'attachment/supervisor_assessment.html', locals())
    
    elif week == 'week 4':
        logbooks = LogBook.objects.filter(date__range=(start + timedelta(days = 22), start + timedelta(days = 29)), student = student).order_by('date')
        try:
            supervisor_comment = SupervisorComment.objects.get(student = student, week = 'week 4')
        except SupervisorComment.DoesNotExist:
            supervisor_comment = None
        print(logbooks)
        return render(request, 'attachment/summary.html', locals())
    
    elif week == 'week 5':
        logbooks = LogBook.objects.filter(date__range=(start + timedelta(days = 29), start + timedelta(days = 36)), student = student).order_by('date')
        try:
            supervisor_comment = SupervisorComment.objects.get(student = student, week = 'week 5')
        except SupervisorComment.DoesNotExist:
            supervisor_comment = None
        print(logbooks)
        return render(request, 'attachment/summary.html', locals())
    
    elif week == 'week 6':
        logbooks = LogBook.objects.filter(date__range=(start + timedelta(days = 36), start + timedelta(days = 43)), student = student).order_by('date')
        try:
            supervisor_comment = SupervisorComment.objects.get(student = student, week = 'week 6')
        except SupervisorComment.DoesNotExist:
            supervisor_comment = None
        print(logbooks)
        return render(request, 'attachment/summary.html', locals())
    
    elif week == 'week 7':
        logbooks = LogBook.objects.filter(date__range=(start + timedelta(days = 43), start + timedelta(days = 50)), student = student).order_by('date')
        try:
            supervisor_comment = SupervisorComment.objects.get(student = student, week = 'week 7')
        except SupervisorComment.DoesNotExist:
            supervisor_comment = None
        print(logbooks)
        return render(request, 'attachment/summary.html', locals())
    
    elif week == 'week 8':
        logbooks = LogBook.objects.filter(date__range=(start + timedelta(days = 50), start + timedelta(days = 57)), student = student).order_by('date')
        try:
            supervisor_comment = SupervisorComment.objects.get(student = student, week = 'week 8')
        except SupervisorComment.DoesNotExist:
            supervisor_comment = None
        print(logbooks)
        return render(request, 'attachment/summary.html', locals())
    
    elif week == 'week 9':
        logbooks = LogBook.objects.filter(date__range=(start + timedelta(days = 57), start + timedelta(days = 64)), student = student).order_by('date')
        try:
            supervisor_comment = SupervisorComment.objects.get(student = student, week = 'week 9')
        except SupervisorComment.DoesNotExist:
            supervisor_comment = None
        print(logbooks)
        return render(request, 'attachment/summary.html', locals())
    
    elif week == 'week 10':
        logbooks = LogBook.objects.filter(date__range=(start + timedelta(days = 64), start + timedelta(days = 71)), student = student).order_by('date')
        try:
            supervisor_comment = SupervisorComment.objects.get(student = student, week = 'week 10')
        except SupervisorComment.DoesNotExist:
            supervisor_comment = None
        print(logbooks)
        return render(request, 'attachment/summary.html', locals())
    
    elif week == 'week 11':
        logbooks =LogBook.objects.filter(date__range=(start + timedelta(days = 71), start + timedelta(days = 78)), student = student).order_by('date')
        try:
            supervisor_comment = SupervisorComment.objects.get(student = student, week = 'week 11')
        except SupervisorComment.DoesNotExist:
            supervisor_comment = None
        print(logbooks)
        return render(request, 'attachment/summary.html', locals())
    
    elif week == 'week 12':
        logbooks = LogBook.objects.filter(date__range=(start + timedelta(days = 78), start + timedelta(days = 85)), student = student).order_by('date')
        try:
            supervisor_comment = SupervisorComment.objects.get(student = student, week = 'week 12')
        except SupervisorComment.DoesNotExist:
            supervisor_comment = None
        print(logbooks)
        return render(request, 'attachment/summary.html', locals())

    logbooks = LogBook.objects.filter(date__range=(start, start + timedelta(days = 8)), student = student).order_by('date')
    try:
        supervisor_comment = SupervisorComment.objects.get(student = student, week = 'week 1')
    except SupervisorComment.DoesNotExist:
            supervisor_comment = None
    return render(request, 'attachment/supervisor_assessment.html', locals())

def staff_logout(request):
    logout(request)
    return redirect('staff-login')

def request_supervision(request):

    if not request.user.updated_profile:
        return redirect('student_registration')
    
    student  = Student.objects.get(user = request.user)
    start_date = mydate.strptime(str(student.start_date), '%Y-%m-%d')
    end_date = mydate.now()
    date_difference = (end_date - start_date).days
    weeks =  date_difference // 7
    if request.method == "POST":
        try:
            supervisor_name = request.POST.get('supervisor')
            supervisor = Lecturer.objects.get(name=supervisor_name)

            supervision(supervisor.user.email, student)
            messages.success(request, 'Request Email sent successfully')
            return redirect('summary')
        except Exception:
            messages.error(request, 'An error occured while sending request!!')
        
    return render(request, 'attachment/request_supervision.html', locals())

## Admin Views
@login_required(login_url='/attachment/staff-login/')
def admin_students(request):
    students = Student.objects.all()
    search_term = request.GET.get('query', '')
    if search_term:
        print(search_term)
        lectures = Lecturer.objects.filter(name__icontains = search_term).values_list('name', flat=True)
        return JsonResponse(list(lectures), safe=False)
    
    if request.method == 'POST':
        try:
            lecturer_name = request.POST.get('supervisor')
            lecturer = Lecturer.objects.get(name = lecturer_name)
            student = Student.objects.get(registration_number = request.POST.get('registration'))
            student.lecturer = lecturer
            student.save()
            return redirect('admin_students')
        except Lecturer.DoesNotExist:
            return HttpResponse("<h5>Lecturer does not exist in the system.</h5>")
    return render(request, 'admin/admin_students.html', locals())

@login_required(login_url='/attachment/staff-login/')
def add_supervisor(request):
    lecturers =  Lecturer.objects.all()
    if request.method == 'POST':
        name =  request.POST.get('name')
        official_email =  request.POST.get('email')
        password = generate_password()
        current_user = User.objects.create(email = official_email, username = name)
        current_user.set_password(password)
        current_user.is_lecturer = True
        current_user.save()
        Lecturer.objects.create(
            name = name,
            official_email =  official_email,
            faculty = request.POST.get('faculty'),
            school = request.POST.get('school'),
            department = request.POST.get('department'), 
            telephone = request.POST.get('telephone'),
            user = current_user
            
        )
        try:
            send_lec_email(official_email, name, password)
        except TimeoutError:
            return JsonResponse({'error':'The was a network error, site took too long to respond'})
        return redirect('add_supervisor')
    return render(request, 'admin/add_supervisor.html', locals())

@login_required(login_url='/attachment/staff-login/')
def view_scores(request):
    students = None
    class_code  = str(request.GET.get('class_code'))
    if class_code.startswith('SCII'):
        students = Student.objects.filter(class_code = class_code)
        return render(request, 'admin/scores.html', locals())

    elif class_code.startswith('SCCJ'):
        students = Student.objects.filter(class_code = class_code)
        return render(request, 'admin/scores.html', locals())

    elif class_code.startswith('SCCI'):
        students = Student.objects.filter(class_code = class_code)
        return render(request, 'admin/scores.html', locals())

    try:
        students = Student.objects.filter( class_code = 'SCII-2019').order_by('class_code')

    except Student.DoesNotExist:
         students = None
    
    return render(request, 'admin/scores.html', locals())

@login_required(login_url='/attachment/staff-login/')
def xls_export(request, code):
    if code.startswith('SCII') or code.startswith('SCCI') or code.startswith('SCCJ') :
        students = Student.objects.filter(class_code = code)

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=students_data.xlsx'

       
        headers = ['NAME', 'REGISTRATION_NUMBER', 'COURSE', 'GRADE']
        workbook = Workbook(response)
        title_format = workbook.add_format({'bold': True, 'font_size': 18, 'font_name': 'Calibri'})
        title_format.set_align('center')
        header_format = workbook.add_format({'bold': True, 'font_name': 'Times New Roman'})
        worksheet = workbook.add_worksheet(f'{code}')
        worksheet.autofit()
        worksheet.write(0, 0, f"{code} EXTERNAL IBL GRADES", title_format)
        worksheet.merge_range(0, 0, 0, len(headers), data=None )
        

        column_widths = {}
        for col_num, header in enumerate(headers):
            worksheet.write(1, col_num, header, header_format)
            column_widths[col_num] = max(len(header), max(len(str(student.__getattribute__(header.lower()))) for student in students))


        data_format = workbook.add_format()
        data_format.set_font_name('Times New Roman')

        for row_num, obj in enumerate(students, 3):
            for col_num, field in enumerate(headers):
                key = field.lower() if field.lower() != 'grade' else obj.grade()
                try:
                    value = str(getattr(obj, key)).upper()
                except AttributeError:
                    value = obj.grade() 
                worksheet.write(row_num, col_num, value, data_format)
                column_widths[col_num] = max(column_widths[col_num], len(str(value)))

        for col_num, width in column_widths.items():
            worksheet.set_column(col_num, col_num, width)
            
        

        workbook.close()
  
        return response

@login_required(login_url='/attachment/staff-login/')
def post_internship(request):

    internships = Internship.objects.all().order_by('-time_stamp')
    
    if request.method == 'POST':
        Internship.objects.create(
            organisation = request.POST.get('organisation'),
            title = request.POST.get('title'),
            url = request.POST.get('url'),
            description = request.POST.get('description'),
            logo = request.FILES.get('logo')

        )
        return redirect('post_internship')

    return render(request, 'admin/post_internship.html', locals())
       
#Lecturer Views
@login_required(login_url='/attachment/staff-login/')
def lec_dashboard(request):
    students = Lecturer.objects.get(user_id = request.user.id).students.all()
    return render(request, 'attachment/lecturer_assessment.html', locals())

@login_required(login_url='/attachment/staff-login/')
def proc_lec_assessment(request, id):
    if request.method == 'POST':
        student = Student.objects.get(user_id = id)
        LecturerAssessment.objects.create(
            respect_to_authority = int(request.POST.get('authority')),
            appearance_grooming = int(request.POST.get('grooming')),
            following_instructions = int(request.POST.get('instruction')),
            enthusiasm = int(request.POST.get('enthusiasm')),
            acheivment = int(request.POST.get('achievment')),
            panctuality = int(request.POST.get('regularity')),
            team_player = int(request.POST.get('team-player')),
            intergration_into_team = int(request.POST.get('working-integration')),
            interaction_ability = int(request.POST.get('interaction')),
            empathy = int(request.POST.get('empathy')),
            safety_awareness = int(request.POST.get('safety-awareness')),
            professional_ethics_application = int(request.POST.get('professional-ethics')),
            current_trends_awareness = int(request.POST.get('current-trends')),
            quality_of_work = int(request.POST.get('work-quality')),
            tasks_completion = int(request.POST.get('task-completion')),
            adopt_new_skills = int(request.POST.get('new-skills')),
            work_competence = int(request.POST.get('work-competence')),
            reliability = int(request.POST.get('reliability')),
            innovation = int(request.POST.get('innovation')),
            written_communication_profiency = int(request.POST.get('written-communication')),
            verbal_communication = int(request.POST.get('verbal-communication')),
            modern_technology = int(request.POST.get('modern-technology')),
            trade_language = int(request.POST.get('trade-language')),
            general_perception = int(request.POST.get('attachee-perception')),
            general_remarks = request.POST.get('lec_remarks'),
            student = student
        )

        student.assessed_by_lecturer = True
        student.save()
        return redirect('lecturer_assessment')

@login_required(login_url='/attachment/staff-login/')
def view_logbook(request):
    students = Lecturer.objects.get(user_id = request.user.id).students.all()   
    return render(request, 'attachment/lecturer_viewlogbook.html', locals())

@login_required(login_url='/attachment/staff-login/')
def proc_view_logbook(request,id):

    student = Student.objects.get(user_id = id)
    default_week = "week 1"
    logbooks = None
    start = student.start_date
    week = request.GET.get('week')

    if week == 'week 1':
        logbooks = LogBook.objects.filter(date__range=(start, start + timedelta(days = 8)), student = student).order_by('date')
        try:
            supervisor_comment = SupervisorComment.objects.get(student = student, week = 'week 1')
        except SupervisorComment.DoesNotExist:
            supervisor_comment = None
        return render(request, 'attachment/lecturer_student_logbook.html', locals())
    elif week == 'week 2':
        logbooks =  LogBook.objects.filter(date__range=(start + timedelta(days = 8), start + timedelta(days = 15)), student = student).order_by('date')
        try:
            supervisor_comment = SupervisorComment.objects.get(student = student, week = 'week 2')
        except SupervisorComment.DoesNotExist:
            supervisor_comment = None
        return render(request, 'attachment/lecturer_student_logbook.html', locals())
    elif week == 'week 3':
        logbooks = LogBook.objects.filter(date__range=(start + timedelta(days = 15), start + timedelta(days = 22)), student = student).order_by('date')
        try:
            supervisor_comment = SupervisorComment.objects.get(student = student, week = 'week 3')
        except SupervisorComment.DoesNotExist:
            supervisor_comment = None
        return render(request, 'attachment/lecturer_student_logbook.html', locals())
    elif week == 'week 4':
        logbooks = LogBook.objects.filter(date__range=(start + timedelta(days = 22), start + timedelta(days = 29)), student = student).order_by('date')
        try:
            supervisor_comment = SupervisorComment.objects.get(student = student, week = 'week 4')
        except SupervisorComment.DoesNotExist:
            supervisor_comment = None
        return render(request, 'attachment/lecturer_student_logbook.html', locals())
    elif week == 'week 5':
        logbooks = LogBook.objects.filter(date__range=(start + timedelta(days = 29), start + timedelta(days = 36)), student = student).order_by('date')
        try:
            supervisor_comment = SupervisorComment.objects.get(student = student, week = 'week 5')
        except SupervisorComment.DoesNotExist:
            supervisor_comment = None
        return render(request, 'attachment/lecturer_student_logbook.html', locals())
    elif week == 'week 6':
        logbooks = LogBook.objects.filter(date__range=(start + timedelta(days = 36), start + timedelta(days = 43)), student = student).order_by('date')
        try:
            supervisor_comment = SupervisorComment.objects.get(student = student, week = 'week 6')
        except SupervisorComment.DoesNotExist:
            supervisor_comment = None
        return render(request, 'attachment/lecturer_student_logbook.html', locals())
    elif week == 'week 7':
        logbooks = LogBook.objects.filter(date__range=(start + timedelta(days = 43), start + timedelta(days = 50)), student = student).order_by('date')
        try:
            supervisor_comment = SupervisorComment.objects.get(student = student, week = 'week 7')
        except SupervisorComment.DoesNotExist:
            supervisor_comment = None
        return render(request, 'attachment/lecturer_student_logbook.html', locals())
    
    elif week == 'week 8':
        logbooks = LogBook.objects.filter(date__range=(start + timedelta(days = 50), start + timedelta(days = 57)), student = student).order_by('date')
        try:
            supervisor_comment = SupervisorComment.objects.get(student = student, week = 'week 8')
        except SupervisorComment.DoesNotExist:
            supervisor_comment = None
        return render(request, 'attachment/lecturer_student_logbook.html', locals())
    
    elif week == 'week 9':
        logbooks = LogBook.objects.filter(date__range=(start + timedelta(days = 57), start + timedelta(days = 64)), student = student).order_by('date')
        try:
            supervisor_comment = SupervisorComment.objects.get(student = student, week = 'week 9')
        except SupervisorComment.DoesNotExist:
            supervisor_comment = None
        return render(request, 'attachment/lecturer_student_logbook.html', locals())
    
    elif week == 'week 10':
        logbooks = LogBook.objects.filter(date__range=(start + timedelta(days = 64), start + timedelta(days = 71)), student = student).order_by('date')
        try:
            supervisor_comment = SupervisorComment.objects.get(student = student, week = 'week 10')
        except SupervisorComment.DoesNotExist:
            supervisor_comment = None
        return render(request, 'attachment/lecturer_student_logbook.html', locals())
    
    elif week == 'week 11':
        logbooks =LogBook.objects.filter(date__range=(start + timedelta(days = 71), start + timedelta(days = 78)), student = student).order_by('date')
        try:
            supervisor_comment = SupervisorComment.objects.get(student = student, week = 'week 11')
        except SupervisorComment.DoesNotExist:
            supervisor_comment = None
        return render(request, 'attachment/lecturer_student_logbook.html', locals())
    
    elif week == 'week 12':
        logbooks = LogBook.objects.filter(date__range=(start + timedelta(days = 78), start + timedelta(days = 85)), student = student).order_by('date')
        try:
            supervisor_comment = SupervisorComment.objects.get(student = student, week = 'week 12')
        except SupervisorComment.DoesNotExist:
            supervisor_comment = None
        return render(request, 'attachment/lecturer_student_logbook.html', locals())

    logbooks = LogBook.objects.filter(date__range=(start, start + timedelta(days = 8)), student = student).order_by('date')
    try:
        supervisor_comment = SupervisorComment.objects.get(student = student, week = 'week 1')
    except SupervisorComment.DoesNotExist:
            supervisor_comment = None
    return render(request, 'attachment/lecturer_student_logbook.html', locals())

@login_required(login_url='/attachment/staff-login/')
def view_report(request):
    students = Lecturer.objects.get(user_id = request.user.id).students.all() 
    return render(request, 'attachment/lecturer_view_report.html', locals())
