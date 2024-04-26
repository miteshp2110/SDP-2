import json

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import UserData,allUser
from django.contrib import messages
@csrf_exempt
def home(request):
    if request.session.get('isAuthenticated'):
        return redirect('/myTasks')

    return render(request,'home.html')
@csrf_exempt
def account(request):
    isAuthenticated=request.session.get("isAuthenticated")
    if(isAuthenticated):
        instance=UserData.objects.get(email=request.session.get('email'))
        length = len(instance.notification['notifications']) + len(instance.connectionRecieved['requests'])
        return render(request,'account.html',{'isAuthenticated':True,'instance':instance,'length':length})
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
@csrf_exempt
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
@csrf_exempt
def notification(request):
    isAuthenticated = request.session.get('isAuthenticated')
    if isAuthenticated:


        instance = UserData.objects.get(email=request.session.get('email'))

        length=len(instance.notification['notifications'])+len(instance.connectionRecieved['requests'])

        return render(request,'notification.html', {'isAuthenticated': isAuthenticated,'instance':instance,'length':length})
    messages.error(request, 'Login first!')
    return redirect('home')

@csrf_exempt
def logout(request):
    request.session.clear()
    return redirect('home')
@csrf_exempt
def activeConnections(request):
    instance=UserData.objects.get(email=request.session.get('email'))
    return render(request,'activeConnections.html',{'instance':instance})
@csrf_exempt
def addConnection(request):
    instance=UserData.objects.get(email=request.session.get('email'))
    instance1=(get_object_or_404(allUser)).userObj['users']
    return render(request,'addConnection.html',{'instance':instance,'instance1':instance1})

@csrf_exempt
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
@csrf_exempt
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
    instanceFrom.save()
    instanceTo.save()


    return redirect('account')
@csrf_exempt

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

        i3=instanceTo.notification['notifications']
        i3.insert(0,request.session.get('email')+" has accepted the Connection request!")
        instanceTo.notification['notifications']=i3

        instanceTo.save()
        instanceFrom.save()

    else:
        instanceTo = get_object_or_404(UserData, email=reqEmail)
        i3 = instanceTo.notification['notifications']
        i3.insert(0, request.session.get('email') + " has Rejected the Connection request!")
        instanceTo.notification['notifications'] = i3
        instanceTo.save()


    instance=get_object_or_404(UserData,email=request.session.get('email'))

    newArr=instance.connectionRecieved['requests']

    filtered_list = [value for value in newArr if value != reqEmail]

    instance.connectionRecieved['requests']=filtered_list
    instance.save()

    instanceX=get_object_or_404(UserData,email=reqEmail)
    ix=instanceX.connectionSent['requests']
    newAr=[value for value in ix if value != request.session.get('email')]
    instanceX.connectionSent['requests']=newAr
    instanceX.save()




    return redirect('notification')

@csrf_exempt
def addTask(request):
    title=request.POST.get('title')
    description=request.POST.get('description')
    deadline=request.POST.get('deadline')
    employed=request.POST.get('employed')

    myObj={'Title':title,'Description':description,'Deadline':deadline,'Employed':employed,'AssignedBy':request.session.get('email'),'Status':"Pending"}
    instance=(get_object_or_404(UserData,email=request.session.get('email')))
    i1=instance.assignedTask['tasks']
    i1.append(myObj)
    instance.assignedTask['tasks']=i1

    instance2=(get_object_or_404(UserData,email=employed))
    i2=instance2.selfTask['tasks']
    i2.append(myObj)
    instance2.selfTask['tasks']=i2

    i3=instance2.notification['notifications']
    i3.insert(0,"You have been assigned a Task by "+request.session.get('email')+" for deadline "+deadline+" .")
    instance2.notification['notifications']=i3
    instance.save()
    instance2.save()


    return redirect('home')

@csrf_exempt
def clrNotification(request):
    num=int(request.POST.get('notificationNumber'))
    instance=get_object_or_404(UserData,email=request.session.get('email'))
    i1=instance.notification['notifications']
    i1.pop(num)
    instance.notification['notifications']=i1
    instance.save()
    return redirect('notification')


def myTasks(request):
    isAuthenticated = request.session.get('isAuthenticated')
    if isAuthenticated:
        instance = UserData.objects.get(email=request.session.get('email'))
        length_AssignedTasks = len(instance.assignedTask['tasks'])
        length = len(instance.notification['notifications']) + len(instance.connectionRecieved['requests'])

        return render(request, 'myTasks.html', {
            'isAuthenticated': True,
            'instance': instance,
            'length': length,
            'taskLength': length_AssignedTasks
        })

    return render(request, 'myTasks.html')


def createTask(request):
    isAuthenticated = request.session.get('isAuthenticated')
    if isAuthenticated:
        instance = UserData.objects.get(email=request.session.get('email'))
        length_AssignedTasks = len(instance.assignedTask['tasks'])
        length = len(instance.notification['notifications']) + len(instance.connectionRecieved['requests'])

        return render(request, 'createTask.html', {
            'isAuthenticated': True,
            'instance': instance,
            'length': length,
            'taskLength': length_AssignedTasks
        })

    return render(request, 'createTask.html')


def assignedTasks(request):
    isAuthenticated = request.session.get('isAuthenticated')
    if isAuthenticated:
        instance = UserData.objects.get(email=request.session.get('email'))
        length_AssignedTasks = len(instance.assignedTask['tasks'])
        length = len(instance.notification['notifications']) + len(instance.connectionRecieved['requests'])

        return render(request, 'assignedTasks.html', {
            'isAuthenticated': True,
            'instance': instance,
            'length': length,
            'taskLength': length_AssignedTasks
        })

    return render(request, 'assignedTasks.html')


def notes(request):
    return render(request, 'notes.html')
