from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from AdminApp.models import Course
import pyttsx3
# Create your views here.

# Index


def talk(data):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 130)
    engine.say(data)
    engine.runAndWait()


def Index(request):
    talk("Home")
    courses = Course.objects.all()
    return render(request, 'index.html', {'courses': courses})
# About


def About(request):
    talk("about us")
    return render(request, 'about.html')
# Courses


def Courses(request):
    talk("courses")
    courses = Course.objects.all()
    return render(request, 'courses.html', {'courses': courses})
# contact


def Contact(request):
    if request.method == 'POST':
        name = request.POST["name"]
        email = request.POST["email"]
        sub = request.POST["subject"]
        msg = request.POST["message"]
        body = f"Name :- {name}\nEmail :- {email}\nMessage : {msg}"
        subject = sub
        send_mail(subject, body, settings.EMAIL_HOST_USER,
                  ['pruthiranjanghose@gmail.com'])
    talk("Contact")
    talk("If any query drop a message to support@betacentauri.com below.")
    return render(request, 'contact.html')

# event-details


def Event_details(request):
    return render(request, 'event-details.html')

# elements


def Elements(request):
    return render(request, 'elements.html')


def error_404(request, exception):
    return render(request, '404.html')
