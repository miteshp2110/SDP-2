from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import adminUser,allUser

def home(request):
    isAuthenticated = request.session.get("isAuthenticated")
    if (isAuthenticated):
        instance = adminUser.objects.get(email=request.session.get('email'))
        aUser=get_object_or_404(allUser)
        return render(request, 'adminHome.html', {'isAuthenticated': True, 'instance': instance,'allUser':aUser})
    else:
        return render(request,'adminHome.html')


def account(request):
    isAuthenticated=request.session.get("isAuthenticated")
    if(isAuthenticated):
        instance=adminUser.objects.get(email=request.session.get('email'))
        return render(request,'adminSignup.html',{'isAuthenticated':True,'instance':instance})
    else:
        if (request.method == "POST"):
            verificationEmail = request.POST.get('email')
            name = request.POST.get('name')
            password = request.POST.get('password')
            if adminUser.objects.filter(email=verificationEmail).exists():
                return HttpResponse("Email already exist")
            else:
                request.session['isAuthenticated'] = True
                request.session['email']=verificationEmail
                newUser = adminUser(email=verificationEmail, name=name, password=password)
                newUser.save()

                return redirect('adminHome')

    return render(request,'adminSignup.html')

def logout(request):
    request.session.clear()
    return redirect('adminHome')

def login(request):

    isAuthenticated = request.session.get('isAuthenticated')
    if (isAuthenticated):

        return redirect('adminHome')
    else:
        if (request.method == "POST"):

            email = request.POST.get('email')
            password = request.POST.get('password')

            if (adminUser.objects.filter(email=email).exists()):
                instance = adminUser.objects.get(email=email).password
                if (instance == password):
                    request.session['isAuthenticated'] = True
                    request.session['email'] = email
                    return redirect('adminHome')

                else:
                    return HttpResponse("wrong password")
            else:
                return HttpResponse("Email does not exist")
    return render(request, 'adminLogin.html')