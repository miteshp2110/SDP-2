from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import UserData

def home(request):
    isAuthenticated = request.session.get("isAuthenticated")
    if (isAuthenticated):
        instance = UserData.objects.get(email=request.session.get('email'))
        return render(request,'home.html',{'isAuthenticated':True,'instance':instance})

    return render(request,'home.html')

def account(request):
    isAuthenticated=request.session.get("isAuthenticated")
    if(isAuthenticated):
        instance=UserData.objects.get(email=request.session.get('email'))
        return render(request,'account.html',{'isAuthenticated':True,'instance':instance})
    else:
        if (request.method == "POST"):
            verificationEmail = request.POST.get('email')
            name = request.POST.get('name')
            password = request.POST.get('password')
            if UserData.objects.filter(email=verificationEmail).exists():
                return HttpResponse("Email already exist")
            else:
                request.session['isAuthenticated'] = True
                request.session['email']=verificationEmail
                newUser = UserData(email=verificationEmail, name=name, password=password)
                newUser.save()
                return redirect('home')

    return render(request,'account.html')

def login(request):
    isAuthenticated=request.session.get('isAuthenticated')
    if(isAuthenticated):
        return redirect('home')
    else:
        if (request.method == "POST"):
            email = request.POST.get('email')
            password = request.POST.get('password')
            if (UserData.objects.filter(email=email).exists()):
                instance = UserData.objects.get(email=email).password
                if (instance == password):
                    request.session['isAuthenticated'] = True
                    request.session['email']=email
                    return redirect('home')

                else:
                    return HttpResponse("wrong password")
            else:
                return HttpResponse("Email does not exist")
    return render(request,'login.html')

def notification(request):


    return render(request,'notification.html')


def logout(request):
    request.session.clear()
    return redirect('home')




