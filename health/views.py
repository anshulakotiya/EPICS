import os
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import easyocr
from django.core.files.storage import FileSystemStorage
from django.template import loader
from validate_email import validate_email
from .models import *
from .forms import *
from health_world.settings import BASE_DIR
import random


def check_mailid(email):
    if validate_email(email):
        return True
    else:
        return False


def password_generator():
    s = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    password = "".join(random.sample(s, 6))
    return password


def home(request):
    return render(request, "home.html")


def signup(request):
    if request.method == "POST":
        image = request.FILES['images']
        fs = FileSystemStorage()
        filepathname = fs.save(image.name, image)
        reader = easyocr.Reader(['en'])
        output = reader.readtext(os.path.join(BASE_DIR, 'media/' + filepathname))
        applicant_name = str(output[6][1])
        card_number = str(output[7][1])
        card_number = card_number[18:]
        mobile_number = output[11][1]
        mobile_number = mobile_number[8:]
        gender = output[10][1]
        gender = gender[8:]
        return render(request, "signup2.html", {'applicant_name': applicant_name, 'card_number': card_number, 'mobile_number': mobile_number, 'gender': gender})
    else:
        return render(request, "signup.html")


def signup2(request):
    if request.method == "POST":
        name = request.POST.get("name")
        card_number = request.POST.get("id_number")
        mobile_number = request.POST.get("mobile_number")
        gender = request.POST.get("gender")
        username = request.POST.get("username")
        password = request.POST.get("password")
        password = make_password(password)
        User(name=name, card_number=card_number, mobile_number=mobile_number, gender=gender, username=username, password=password).save()
        return HttpResponse("User Generate successfully")
    else:
        return render(request, "signup.html")


def emailValidation(request):
    otp = request.POST.get('otp')
    if request.session['otp'] == otp:
        return HttpResponse('valid')
    else:
        return HttpResponse('not valid')


def emailGeneration(request):
    entered_email = request.POST.get('email')
    if check_mailid(entered_email):
        all_users = User.objects.all()
        for single_user in all_users:
            if str(single_user.username) == entered_email:
                return HttpResponse('not unique')
        else:
            otp = password_generator()
            request.session['otp'] = otp
            html_message = loader.render_to_string('emails/otp_email.html', {'otp': otp})
            mail = send_mail('Email Verification', '', settings.EMAIL_HOST_USER, [entered_email],
                             html_message=html_message,
                             fail_silently=False)
            if mail:
                return HttpResponse('send')
            else:
                return HttpResponse('not send')
    else:
        return HttpResponse('not valid')

def loginpage(request):
    form = loginForm()
    return render(request, 'loginpage.html', {'form': form})