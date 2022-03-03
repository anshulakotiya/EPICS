import random
import easyocr
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.hashers import make_password
from django.contrib.messages import error
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader

from .models import *


def password_generator():
    s = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    password = "".join(random.sample(s, 6))
    return password


def captcha_generator():
    s = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    captcha = "".join(random.sample(s, 6))
    return captcha


def random_quotes():
    quotes_list = ["Your health is an investment, not expense.", "Regular exercise keeps you healthy.", "our 'HEALTH' should be the priority always.",
                   "One day you will get there, until then train as hard as you can.", "Let go of harmful habits that do not serve you!",
                   "our health is your greatest gift. Never take it for granted!", "et goals ,stay focused , never give up and stay healthy!",
                   "Genius is the one who has abundance of life and health!", "It is health that is real wealth.", "The first wealth is health.",
                   "When you focus on your health, you awaken your creativity and ability to conceive better life.",
                   "The best doctors: sunshine, water, prayer, rest, quality food, and exercise.", "You 'GLOW' differently when you are actually 'HEALTHY'.",
                   "Where there is health, there is a way to everything.", "Healthy is an outfit that looks beautiful on everyone.",
                   "Exercise changes your body,  your mind, your attitude and your mood.", "Exercise should be regarded as a tribute to the heart.",
                   "Good things come to those who sweat.", "Take care of your body. It's the only place you have to live.", "Invest in yourself, for yourself.",
                   "Who has health has hope and who has hope has everything.", "Your body will be around a lot longer than that expensive handbag.",
                   "Reading is to the mind what exercise is to the body.", "A healthy outside starts from the inside.", "Health is the vital principle of bliss.",
                   "All progress takes place outside the comfort zone.", "The groundwork for all happiness is good health.",
                   "Exercise is king. Nutrition is queen. Put them together and you’ve got a kingdom.", "Your body is your most priceless passion!",
                   "Health is the bridge between goals and accomplishment.", "The pain you feel today will be the strength you feel tomorrow.",
                   " Being healthy is the foundational key to all success.", "Setting goals is the first step into turning the invisible into the visible.",
                   "Your body is the church where Nature asks to be reverenced.", "Get comfortable with being uncomfortable!", "No pain, no gain.",
                   "You shall gain, but you shall pay with sweat, blood.", "There’s no secret formula. I lift heavy, work hard, and aim to be the best.",
                   "Health and motivation determines what you do.", "Don’t count the days, make the days count.", "Getting fit is all about mind over matter.",
                   "All great achievements require time and mental fitness!", "To enjoy the glow of good health, you must exercise.",
                   "Every champion was once a contender that refused to give up.", "Fitness is not a destination, it's a way of life.",
                   "Wellness is a collection of paths, knowledge and action.", "Your health is your best friend .",
                   "Don't decrease the goals instead increase your efforts.", "Every human being is the author of his own health.",
                   "We cannot become what we want by remaining what we are!!"]
    return random.choice(quotes_list)


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
        id = HealthCard.objects.create(card=image).id
        my_image = HealthCard.objects.get(id=id).card.url
        reader = easyocr.Reader(['en'])
        output = reader.readtext(my_image)
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
        return redirect("/")
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


def user_login(request):
    user = request.user
    quote = random_quotes()
    return render(request, 'user.html', {'user_name': user, 'quote': quote})


def signup_doctor(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        password = make_password(password)
        name = request.POST.get('name')
        gender = request.POST.get('gender')
        phone_number = request.POST.get('phone_number')
        licence_no = request.POST.get('licence_no')
        licence_image = request.FILES['image1']
        u_instance = User.objects.create(username=username, password=password, name=name, gender=gender, phone_number=phone_number, is_doctor=True, is_active=False)
        doctorLicence(user_id=u_instance, licence_no=licence_no, licence_image=licence_image).save()
        return render(request, 'doctor_after_signup.html')
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
