from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import uuid
from .models import *
from django.core.mail import send_mail
from django.contrib.auth import settings
import os


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password1')
        user = authenticate(username=username, password=password)
        if user is not None:
            prof = Profile.objects.get(user=user)
            if prof.is_verified == True:
                login(request, user)
                return redirect('home')
            else:
                return redirect('error')
        else:
            messages.error(request, 'invalid password')
            return redirect('login')
    else:
        return render(request, 'login.html', locals())


def success(request):
    return render(request, 'success.html')

def logout_page(request):
    logout(request)
    messages.error(request, "you are logged out..")
    return redirect("login")
def registration(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if username is not None:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'username is exists,please try another')
                return redirect('registration')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'email is exists,please try another')
                return redirect('registration')
            else:
                if password1 == password2:
                    user = User.objects.create_user(
                        first_name=first_name,
                        last_name=last_name,
                        username=username,
                        email=email,
                        password=password1,
                    )
                    user.save()
                    auth_token = str(uuid.uuid4())
                    pro_obj = Profile.objects.create(user=user, auth_token=auth_token)
                    pro_obj.save()
                    send_mail_registration(email, auth_token)
                    messages.success(request, 'successfully registration done')
                    return redirect('success')
                else:
                    messages.error(request, "your given password doesn't match....")
                    return redirect('registration')
    else:
        return render(request, 'registration.html', locals())


def send_mail_registration(email, auth_token):
    subjects = 'your Account Authentication link'
    message = f'hi please click here to verify your account:http://127.0.0.1:8000/verify/{auth_token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subjects, message, email_from, recipient_list)


def verify(request, auth_token):
    profile_obj = Profile.objects.filter(auth_token=auth_token).first()
    profile_obj.is_verified = True
    profile_obj.save()
    messages.success(request, 'Congratulation Account Verify Its done')
    return redirect('login')


def new_pass(request):
    return render(request, 'new_pass.html')



def reset_pass(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user_prof = User.objects.get(email=email)
        res_prof = Profile.objects.get(user=user_prof)
        auth_token = res_prof.auth_token
        print(auth_token)
        send_mail_reset(email, auth_token)
        return redirect('success1')
    return render(request, 'reset_pass.html')


def send_mail_reset(email, auth_token):
    subjects = 'your Account Reset password link'
    message = f'hi please click here to reset your Password:http://127.0.0.1:8000/reset_user_pass/{auth_token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subjects, message, email_from, recipient_list)


def reset_user_pass(request, auth_token):
    profile_obj = Profile.objects.filter(auth_token=auth_token).first()
    if profile_obj:
        if request.method == 'POST':
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            if password1 == password2:
                user = profile_obj.user
                user.set_password(password1)
                user.save()
                messages.success(request, 'your password successfully changed')
                return redirect('login')
            else:
                messages.error(request, 'your password and retype your password is not matched')
    return render(request, 'new_pass.html')


def error(request):
    return render(request, 'error.html')


def success1(request):
    return render(request, 'success1.html')


def home(request):
    user_prof = Userprofile.objects.all()
    return render(request, 'home.html', locals())


def create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        image = request.FILES.get('image')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        note=request.POST.get('note')
        if name:
            if image:
                prof = Userprofile.objects.create(
                    name=name,
                    image=image,
                    email=email,
                    phone_number=phone_number,
                    note=note,

                )
                prof.save()
                messages.success(request, 'profile updated.............')
                return redirect('home')
            else:
                prof = Userprofile.objects.create(
                    name=name,
                    email=email,
                    phone_number=phone_number,
                    note=note,
                )
                prof.save()
                messages.success(request, 'profile updated.............')
                return redirect('home')
        else:
            messages.error(request, 'please fill up all fields.....')

    return render(request, 'create.html', locals())


def delete(request, id):
    prof = Userprofile.objects.get(id=id)
    if prof.image.name != 'default_pic/def.png':
        if os.path.exists(prof.image.path):
            os.remove(prof.image.path)
    prof.delete()
    return redirect('home')


def see_profile(request, id):
    prof = Userprofile.objects.get(id=id)
    return render(request, 'see_profile.html', locals())


def update_profile(request, id):
    prof = Userprofile.objects.get(id=id)
    if request.method == 'POST':
        if request.FILES.get('image') != None:
            if prof.image != 'default/def.jpg':
                if os.path.exists(prof.image.path):
                    os.remove(prof.image.path)

            prof.name = request.POST['name']
            prof.image = request.FILES.get('image')
            prof.email = request.POST.get('email')
            prof.phone_number = request.POST.get('phone_number')
            prof.note = request.POST.get('note')
            prof.save()
            messages.success(request, "Profile details Updated.")
            return redirect('home')
        else:
            prof.name = request.POST.get('name')
            prof.Email = request.POST.get('Email')
            prof.age = request.POST.get('age')
            prof.phone_number = request.POST.get('phone_number')
            prof.note = request.POST.get('note')
            prof.save()
            messages.success(request, "Profile details Updated.")
            return redirect('home')
    return render(request, 'update_profile.html', locals())
