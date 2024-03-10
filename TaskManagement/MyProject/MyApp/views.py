import json

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import UserData,allUser
from django.contrib import messages

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
                instance=get_object_or_404(allUser)
                arr=(instance.userObj)['users']
                arr.append(verificationEmail)
                (instance.userObj)['users']=arr
                instance.save()
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
    isAuthenticated = request.session.get('isAuthenticated')
    if isAuthenticated:
        instance = UserData.objects.get(email=request.session.get('email'))
        return render(request,'notification.html', {'isAuthenticated': isAuthenticated,'instance':instance})
    messages.error(request, 'Login first!')
    return redirect('home')


def logout(request):
    request.session.clear()
    return redirect('home')

def activeConnections(request):
    instance=UserData.objects.get(email=request.session.get('email'))
    return render(request,'activeConnections.html',{'instance':instance})

def addConnection(request):
    instance=UserData.objects.get(email=request.session.get('email'))
    instance1=(get_object_or_404(allUser)).userObj['users']
    return render(request,'addConnection.html',{'instance':instance,'instance1':instance1})


def feedback(request):
    isAuthenticated = request.session.get('isAuthenticated')
    if isAuthenticated:
        if request.method == 'POST':
            messages.error(request, 'Feedback sent successfully!')
            return redirect('home')
        else:
            return render(request,'feedback.html')
    messages.error(request, 'Login first!')
    return redirect('home')

def processRequest(request):
    reqEmail=request.POST.get('reqEmail')
    print(reqEmail)
    instanceTo=get_object_or_404(UserData,email=reqEmail)
    instanceFrom=get_object_or_404(UserData,email=request.session.get('email'))
    print('insFrom: ',instanceFrom.name," insTo: ",instanceTo.name)
    i1=instanceFrom.connectionSent['requests']
    i2=instanceTo.connectionRecieved['requests']
    i1.append(reqEmail)
    i2.append(request.session.get('email'))
    instanceFrom.connectionSent['requests']=i1
    instanceTo.connectionRecieved['requests']=i2
    instanceTo.save()
    instanceFrom.save()

    return redirect('account')


def acceptRequest(request):
    reqEmail=request.POST.get('reqEmail')
    pType=request.POST.get('type')

    if(pType=='1'):
        print("acc")
        instanceTo = get_object_or_404(UserData, email=reqEmail)
        instanceFrom = get_object_or_404(UserData, email=request.session.get('email'))
        i1=instanceTo.activeConnections['connections']
        i2=instanceFrom.activeConnections['connections']

        i1.append(request.session.get('email'))
        i2.append(reqEmail)




        instanceTo.activeConnections['connections']=i1
        instanceFrom.activeConnections['connections']=i2

        instanceTo.save()
        instanceFrom.save()

    instance=get_object_or_404(UserData,email=request.session.get('email'))

    newArr=instance.connectionRecieved['requests']

    filtered_list = [value for value in newArr if value != reqEmail]

    instance.connectionRecieved['requests']=filtered_list
    instance.save()




    return redirect('notification')


def addTask(request):
    title=request.POST.get('title')
    description=request.POST.get('description')
    deadline=request.POST.get('deadline')
    employed=request.POST.get('employed')

    myObj={'Title':title,'Description':description,'Deadline':deadline,'Employed':employed,'AssignedBy':request.session.get('email')}
    instance=(get_object_or_404(UserData,email=request.session.get('email')))
    print(instance.assignedTask)
    i1=instance.assignedTask['tasks']
    i1.append(myObj)
    print(i1)
    instance.assignedTask['tasks']=i1
    instance.save()





    return redirect('home')




