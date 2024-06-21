from email.message import EmailMessage
from .password_generator import generate_password
from .models import User, OrganisationSupervisor
import smtplib
import ssl
def send_orgs_email(supervisor_email,supervisor_name, student):
    sender = 'karanide001@gmail.com'
    email_password ='zmjvvafgnmuevvgj'
    subject = 'Student Assessment'
    body = None
    try:
        existing_user = User.objects.get(email = supervisor_email)
        existing_supervisor = existing_user.organisationsupervisor
        student.supervisor = existing_supervisor
        student.save()
        body = f"""Hello {existing_user.username},
Follow the link below to assesss {student.name}.
Link: http://127.0.0.1:8000/attachment/staff-login/
Warmest Regards,
{student.name}.
"""
    except User.DoesNotExist:
        password = generate_password()
        myuser = User.objects.create(email=supervisor_email, username=supervisor_name)
        myuser.is_supervisor = True
        myuser.set_password(password)
        myuser.save()
        supervisor = OrganisationSupervisor.objects.create(user=myuser)
        student.supervisor = supervisor
        student.save()
        body = f"""Hello {myuser.username},
Here is the the login link to assess {student.name}.
Link: http://127.0.0.1:8000/attachment/staff-login/
password: {password}
Warmest Regards,
{student.name}.
"""
    
    email = EmailMessage()
    email['From'] = sender
    email['To'] = supervisor_email
    email['subject'] = subject
    email.set_content(body)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(sender, email_password)
        smtp.sendmail(sender, supervisor_email, email.as_string() )

def send_lec_email(lec_email, name, credentials):
    sender = 'karanide001@gmail.com'
    email_password ='zmjvvafgnmuevvgj'
    subject = 'Account Created'
    body = f"""Hello {name},
Here is the the login link:
Link: http://127.0.0.1:8000/attachment/staff-login/
password: {credentials}
Warmest Regards,
Admin.
"""
    email = EmailMessage()
    email['From'] = sender
    email['To'] = lec_email
    email['subject'] = subject
    email.set_content(body)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(sender, email_password)
        smtp.sendmail(sender, lec_email, email.as_string())

def supervision(supervision_email, student):
    sender = 'karanide001@gmail.com'
    email_password ='zmjvvafgnmuevvgj'
    subject = 'Student Assessment'
    body = f"""Greetings, 
Hope your are having a great day, {student.name} of registration number 

{student.registration_number}, is requesting for supervision at {student.organisation}, 

for further communication with the student you can contact him/her at {student.user.email}.

Warm Regards,
{student.name}
    
"""
    email = EmailMessage()
    email['From'] = sender
    email['To'] = supervision_email
    email['subject'] = subject
    email.set_content(body)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(sender, email_password)
        smtp.sendmail(sender, supervision_email, email.as_string())
