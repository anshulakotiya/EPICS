import os
import random
import easyocr
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.hashers import make_password
from django.contrib.messages import error
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from validate_email import validate_email

from health_world.settings import BASE_DIR
from .models import *


def check_mailid(email):
    if validate_email(email):
        return True
    else:
        return False


def password_generator():
    s = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    password = "".join(random.sample(s, 6))
    return password


def captcha_generator():
    s = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    captcha = "".join(random.sample(s, 6))
    return captcha


def home(request):
    if request.session.has_key('logged_in_as_user'):
        return redirect('/login/patient/')
    elif request.session.has_key('logged_in_as_doctor'):
        return render(request, 'doctor.html')
    elif request.session.has_key('logged_in_as_technical'):
        return render(request, 'technical.html')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if user.is_user:
                auth.login(request, user)
                request.session['logged_in_as_user'] = True
                return redirect('/login/patient/')
            elif user.is_doctor:
                auth.login(request, user)
                request.session['logged_in_as_doctor'] = True
                return render(request, 'doctor.html')
            elif user.is_technical:
                auth.login(request, user)
                request.session['logged_in_as_technical'] = True
                return render(request, 'technical.html')
        else:
            error(request, 'invalid credentials')
    captcha = password_generator()
    request.session['captcha'] = captcha
    return render(request, "home.html", {'captcha': captcha})

def refreshCaptcha(request):
    captcha = password_generator()
    request.session['captcha'] = captcha
    return HttpResponse(captcha)

def signup(request):
    if request.method == "POST":
        image = request.FILES['images']
        fs = FileSystemStorage()
        filepathname = fs.save(image.name, image)
        reader = easyocr.Reader(['en'])
        output = reader.readtext(os.path.join(BASE_DIR, 'media/' + filepathname))
        health_card = output[5][1]
        if health_card != "Health Id":
            applicant_name = str(output[6][1])
            card_number = str(output[7][1])
            card_number = card_number[18:]
            try:
                card_no = User.objects.get(card_number=card_number)
                error(request, 'This card already exist')
                return render(request, "signup.html", {'card_no': card_no})
            except ObjectDoesNotExist:
                phr_address = str(output[8][1])
                phr_address = phr_address[13:]
                mobile_number = output[11][1]
                mobile_number = mobile_number[8:]
                gender = output[10][1]
                gender = gender[8:]
                return render(request, "signup2.html",
                              {'applicant_name': applicant_name, 'card_number': card_number, 'mobile_number': mobile_number, 'gender': gender,
                               'phr_address': phr_address})
        else:
            error(request, 'You uploaded the wrong card')
    return render(request, "signup.html")


def signup2(request):
    if request.method == "POST":
        name = request.POST.get("name")
        card_number = request.POST.get("id_number")
        phr_address = request.POST.get('phr_address')
        phone_number = request.POST.get("mobile_number")
        gender = request.POST.get("gender")
        username = request.POST.get("username")
        password = request.POST.get("password")
        password = make_password(password)
        User(name=name, card_number=card_number, phr_address=phr_address, phone_number=phone_number, gender=gender, username=username, password=password,
             is_user=True).save()
        return render(request, "successful_signup.html")
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
        print(all_users)
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


def user_login(request):
    user = request.user
    return render(request, 'user.html', {'user_name': user})


def signup_doctor(request):
    return render(request, 'signup_doctor.html')


def logout(request):
    auth.logout(request)
    return redirect('/')


def forgot_password(request):
    return render(request, 'forgot_password.html')


def forgot_password_otp(request):
    email = request.POST.get('email')
    try:
        users = User.objects.get(username=email)
        otp = password_generator()
        request.session['otp'] = otp
        html_message = loader.render_to_string('emails/forgot_pass.html', {'otp': otp})
        mail = send_mail('Email Verification', '', settings.EMAIL_HOST_USER, [email],
                         html_message=html_message,
                         fail_silently=False)
        if mail:
            return HttpResponse(otp)
        else:
            return HttpResponse('not send')
    except ObjectDoesNotExist:
        return HttpResponse("not exist")


def signup_doctor_ajax(request):
    email = request.POST.get("email")
    try:
        users = User.objects.get(username=email)
        return HttpResponse("already exist")
    except ObjectDoesNotExist:
        otp = password_generator()
        request.session['doctor_signup_otp'] = otp
        html_message = loader.render_to_string('emails/otp_email.html', {'otp': otp})
        mail = send_mail('Email Verification', '', settings.EMAIL_HOST_USER, [email],
                         html_message=html_message,
                         fail_silently=False)
        if mail:
            return HttpResponse("send")
        else:
            return HttpResponse('not send')


def doctorEmailValidation(request):
    otp = request.POST.get('otp')
    if request.session['doctor_signup_otp'] == otp:
        return HttpResponse('valid')
    else:
        return HttpResponse('not valid')
