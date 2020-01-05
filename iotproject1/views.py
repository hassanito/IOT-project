from django.urls import reverse
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render
import datetime
from django.shortcuts import render_to_response
from django.utils import timezone
from .models import Student,ApptRequests,Professor

from django.conf import settings
from django.core.mail import send_mail

#USER CELERY FOR PERIODIC FUNCTIONS
import paho.mqtt.client as mqtt


def test(request):
    if request.method == "POST":
        student_email = request.POST.get('email')
        pr = request.POST.get('professor')
        time = datetime.datetime.now().time()
        date = datetime.datetime.now().date()
        print("the user email is "+student_email+" and he wants to see "+pr)
        print(date)
        prof = Professor.objects.get(professor = pr)
        new_student = Student(email=student_email,date_time=timezone.now(),professor = prof)
        new_student.save()
        appt = ApptRequests(professor = prof,student= new_student)
        appt.save()
        if(get_state_from_db(pr)==True):
            send_presence_mail(appt.get_time(),new_student,prof)
        else:
            send_absence_mail(appt.get_time(),new_student,prof)

        print(prof)
        print(new_student)
        print(appt)
        print(appt.get_time())

    return render(request,'iotproject1/home.html')





def get_state_from_db(pr):
    prof = Professor.objects.get(professor = pr)
    #this function will rerturn the current state that is saved from the model
    return prof.in_office


def delete_old_requests():
    #this function checks all the ApptRequests and Students that have been in the DB
    #for more than 24 hours and delete them
    import datetime,pytz
    now_utc = pytz.utc.localize(datetime.datetime.utcnow())
    for appt in ApptRequests.objects.all():
        if(now_utc.day - appt.get_time().day >=1 ):
            appt.delete()


def send_presence_mail(time,student,professor):
    #this function sends an email to the student about the presence of a certain professor
    print("mail sending")
    subject = professor.professor +" is in office now "
    time = " this message was sent at "+ str(time)
    student_email = student.email
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [student_email,]
    send_mail('professor presence',subject +time , email_from, recipient_list )


def send_absence_mail(time,student,professor):
    print("mail sending")
    subject = professor.professor +" is not in office now "
    time = " this message was sent at "+ str(time)
    student_email = student.email
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [student_email,]
    send_mail('professor presence',subject +time , email_from, recipient_list)
