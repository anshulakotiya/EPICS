import random

import easyocr
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.messages import error, success
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.core.management import call_command
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.template import loader

from .forms import *


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


def home(request):
    if request.session.has_key('logged_in_as_user'):
        return redirect('/login/patient/')
    elif request.session.has_key('logged_in_as_doctor'):
        return redirect('/login/doctor/')
    elif request.session.has_key('logged_in_as_technical'):
        return redirect('/login/technical/')
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
                return redirect('/login/doctor/')
            elif user.is_technical:
                auth.login(request, user)
                request.session['logged_in_as_technical'] = True
                return redirect('/login/technical/')
        else:
            error(request, 'invalid credentials')
    captcha = password_generator()
    request.session['captcha'] = captcha
    return render(request, "home.html", {'captcha': captcha})


@login_required(login_url='/')
def technical(request):
    return render(request, 'technical.html')


@login_required(login_url='/')
def doctor(request):
    return render(request, 'doctor.html')


@login_required(login_url='/')
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


@login_required(login_url='/')
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
        return HttpResponse(users + "already exist")
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


def doctors_verification(request):
    doctor_to_verify = doctorLicence.objects.filter(user_id__is_active=False, user_id__is_doctor=True)
    return render(request, 'doctors_verification.html', {'doctor_to_verify': doctor_to_verify})


@login_required(login_url='/')
def upload_document(request):
    if request.method == "POST":
        my_form = uploadDocumentForm(request.POST)
        if my_form.is_valid():
            ins = my_form.save(commit=False)
            ins.user = request.user
            ins.save()
            print(ins.id)
            url = '/login/patient/upload_document_2/' + str(ins.id)
            return redirect(url)
    else:
        form = uploadDocumentForm()
        return render(request, 'upload_document.html', {'form': form})


@login_required(login_url='/')
def upload_document_2(request, id):
    if request.method == "POST":
        report = request.POST.get('report')
        report_date = request.POST.get('date')
        text = request.POST.get('text')
        Documents(file=report, userDis=UserDisease.objects.get(id=id), date=report_date, text=text).save()
    data = UserDisease.objects.get(id=id)
    # all_files = Documents.objects.filter(userDis=id)
    return render(request, 'upload_document_2.html', {'data': data, 'id': id})


@login_required(login_url='/')
def view_document(request):
    all_disease = UserDisease.objects.filter(user=request.user)
    return render(request, 'view_document.html', {'all_disease': all_disease})


@login_required(login_url='/')
def view_document_2(request, id):
    disease = UserDisease.objects.get(id=id)
    print(disease)
    all_reports = Documents.objects.filter(userDis=disease)
    print(all_reports)
    return render(request, 'view_document_2.html', {'id': id, 'disease': disease, 'all_reports': all_reports})


@login_required(login_url='/')
def get_backup(request):
    try:
        call_command('dbbackup')
        success(request, "Backup Completed!")
    except:
        error(request, "Backup Not Completed")
    return redirect('/login/technical/')


@login_required(login_url='/')
def phr_address(request):
    if request.method == "POST":
        phr_add = request.POST.get('phr_address')
        try:
            searched_user = User.objects.get(is_active=True, phr_address=phr_add, is_user=True)
            user_disease = UserDisease.objects.filter(user=searched_user)
            return render(request, 'search_result.html', {'searched_user': searched_user, 'user_disease': user_disease})
        except ObjectDoesNotExist:
            error(request, "Please enter the correct details")
            return redirect('/login/doctor/')


@login_required(login_url='/')
def health_id(request):
    if request.method == "POST":
        health_id_no = request.POST.get('health_id')
        try:
            searched_user = User.objects.get(is_active=True, card_number=health_id_no, is_user=True)
            user_disease = UserDisease.objects.filter(user=searched_user)
            return render(request, 'search_result.html', {'searched_user': searched_user, 'user_disease': user_disease})
        except ObjectDoesNotExist:
            error(request, "Please enter the correct details")
            return redirect('/login/doctor/')


def doctors_verification_completed(request, id):
    print(User.objects.get(id=id))
    my_user = User.objects.get(id=id)
    my_user.is_active = True
    my_user.save()
    return redirect(doctors_verification)


@login_required(login_url='/')
def edit_document(request, id):
    raise Http404("Page under development")


@login_required(login_url='/')
def delete_document(request, id):
    raise Http404("Page under development")


@login_required(login_url='/')
def view_user_document(request, id):
    disease = UserDisease.objects.get(id=id)
    print(disease)
    all_reports = Documents.objects.filter(userDis=disease)
    print(all_reports)
    return render(request, 'view_document_2.html', {'id': id, 'disease': disease, 'all_reports': all_reports})
