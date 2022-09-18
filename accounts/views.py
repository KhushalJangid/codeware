from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User
# from accounts.models import
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from accounts.models import Key,User
from accounts.verify import get_otp, send_otp
from time import perf_counter
from threading import Thread
from uuid import uuid4
# Create your views here.

def loginUser(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = User.objects.get(email=email)
        except Exception as e:
            messages.error(request,'Email not registered. Please signin first.')
            return render(request, "accounts/login.html")
        password = request.POST.get("password")
        user = authenticate(id=user.id, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            # print("user not found \n")
            messages.error(request,'Incorrect Password')
            return render(request, "accounts/login.html")

    else:
        return render(request, "accounts/login.html")

def signin(request):
    
    # if request.method == "POST" and 'verify' in request.POST:
    #     otp = request.POST.get('otp')
    #     try:
    #         OTP = request.session['otp']
    #         start = request.session['instance']
    #     except KeyError:
    #         return redirect("/account/signup")
    #     if OTP == otp:
    #         if (perf_counter()-start) <= 600:
    #             uid = request.session['uid']
    #             user = User.objects.get(id=uid)
    #             user.is_active = True
    #             user.save()
    #             login(request, user,
    #                   backend='django.contrib.auth.backends.ModelBackend')
    #             return redirect("/")
    #         else:
    #             messages.error(request,"OTP expired")
    #             return redirect("/account/signin")
    #     else:
    #         messages.error(request,'OTP does not match')
    #         return render(request, 'accounts/verify.html')
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password0 = request.POST.get("password0")
        name = name.split()
        if password == password0:
            try :
                user = User.objects.create_user(first_name=name[0], last_name=name[-1],
                                            email=email, password=password, is_active=False)
            except Exception as e:
                print(e)
                user = User.objects.get(email=email)
                if user.is_active:
                    messages.error(request, 'User Already Exists.')
                    return redirect("/accounts/signup")
                user.is_active = True
                user.save()
                return redirect("/")
            # # user.save()
            # OTP = get_otp()
            # send_otp(email, OTP,f'{name[0]} {name[-1]}')
            # request.session['uid'] = user.id
            # request.session['otp'] = OTP
            # request.session['instance'] = perf_counter()
            # return render(request, 'accounts/verify.html')
        else:
            messages.error(request, 'Your Password Does not match.')
            return redirect("/accounts/signup")
    else:
        return render(request, "accounts/signup.html")

def forgot(request):
    if request.method == "POST" and "send-mail" in request.POST:
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            OTP = get_otp()
            request.session['otp'] = OTP
            request.session["email"] = email
            var = Thread(target=send_otp, args=(
                email, OTP, f"{user.first_name} {user.last_name}"), daemon=True)
            var.start()
            return render(request,"accounts/verify.html")
        except :
            messages.error(request,"User with the Email does not exists!")
            return render(request,"accounts/forgot.html")
    elif request.method == "POST" and "verify" in request.POST:
        otp = request.POST.get("otp") 
        OTP = request.session['otp']
        if otp == OTP:
            return render(request,"accounts/forgot.html",{"reset":True})
        else:
            messages.error(request,"Wrong OTP !")
            return render(request,"accounts/verify.html")
    elif request.method == "POST" and "submit" in request.POST:
        password = request.POST.get("password")
        password0 = request.POST.get("password0")
        if password == password0:
            email = request.session['email']
            User.objects.get(email=email).set_password(password)
            return redirect("/login")
        else:
            messages.error(request,"Passwords do not match !")
            return render(request,"accounts/forgot.html",{"reset":True})
    return render(request,"accounts/forgot.html")

@login_required
def reset(request):
    if request.method == "POST":
        password = request.POST.get('password')
        password0 = request.POST.get('password0')
        newpassword = request.POST.get('newpassword')
        if password0 == password:
            user = request.user
            user_exist = authenticate(id=user.id, password=password)
            if user_exist:
                user.set_password(newpassword)
            else:
                messages.error(request,"Wrong password !")
                return redirect("/accounts/reset-password") 
        else:
            messages.error(request,"Passwords do not match !")
            return redirect("/accounts/reset-password")
    return render(request,"accounts/reset.html",{"var":True})

@login_required
def logoutUser(request):
    logout(request)
    return redirect("/")

@login_required
def change_email(request):
    if request.method == "POST" and "submit" in request.POST:
        n_email = request.POST.get("email")
        user =request.user
        OTP = get_otp()
        request.session['otp'] = OTP
        request.session["email"] = n_email
        request.session["id"] = user.id
        var = Thread(target=send_otp, args=(
            n_email, OTP, f"{user.first_name} {user.last_name}"), daemon=True)
        var.start()
        return render(request,"accounts/verify.html",{"var":True})
    elif request.method == "POST" and "verify" in request.POST:
        otp = request.POST.get("otp")
        OTP = request.session["otp"]
        n_email = request.session["email"]
        if otp == OTP:
            id = request.session["id"]
            user = User.objects.get(id=id)
            user.email=n_email
            user.save()
            return redirect("/")
        else:
            messages.error(request,"Wrong OTP !")
            return render(request,"accounts/verify.html",{"var":True})
    else:
        return render(request,"accounts/change_email.html",{"var":True})

def verify(request):
    pass