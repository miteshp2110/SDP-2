import datetime
import json

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
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
            feed=request.POST.get('comments')
            instance=get_object_or_404(allUser)
            i1=instance.feedback['feedbacks']
            i1.insert(0,feed)
            instance.feedback['feedbacks']=i1
            instance.save()
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

    messages.success(request, 'Task created and assigned successfully!')
    return redirect('/assignedTasks')

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
        length = len(instance.notification['notifications']) + len(instance.connectionRecieved['requests'])
        return render(request, 'myTasks.html', {
            'instance': instance,
            'length': length,
        })

    return render(request, 'myTasks.html')


def createTask(request):
    isAuthenticated = request.session.get('isAuthenticated')
    if isAuthenticated:
        instance = UserData.objects.get(email=request.session.get('email'))
        length = len(instance.notification['notifications']) + len(instance.connectionRecieved['requests'])

        return render(request, 'createTask.html', {
            'instance': instance,
            'length': length,
        })

    return render(request, 'createTask.html')


def assignedTasks(request):
    isAuthenticated = request.session.get('isAuthenticated')
    if isAuthenticated:
        instance = UserData.objects.get(email=request.session.get('email'))
        length = len(instance.notification['notifications']) + len(instance.connectionRecieved['requests'])

        return render(request, 'assignedTasks.html', {
            'instance': instance,
            'length': length,
        })

    return render(request, 'assignedTasks.html')


def notes(request):
    isAuthenticated = request.session.get('isAuthenticated')
    if isAuthenticated:
        instance = UserData.objects.get(email=request.session.get('email'))
        length = len(instance.notification['notifications']) + len(instance.connectionRecieved['requests'])
        notes=instance.notes.get('notes')

        return render(request, 'notes.html', {
            'instance': instance,
            'length': length,
            'notes':notes
        })

    return render(request, 'notes.html')

@csrf_exempt
def deleteTask(request):
    if(request.method=="POST"):
        deletionId=(json.loads(request.body)).get('deletionId')
        instance = get_object_or_404(UserData, email=request.session.get('email'))
        assignedTask = (instance.assignedTask).get('tasks')
        task_to_delete = assignedTask[deletionId]
        deletion_instance = get_object_or_404(UserData, email=task_to_delete.get('Employed'))
        deletion_task = deletion_instance.selfTask.get('tasks')

        count = 0
        for obj in deletion_task:
            count += 1
            if ((obj.get('Title') == task_to_delete.get('Title')) and (
                    obj.get('Description') == task_to_delete.get('Description')) and (
                    obj.get('Deadline') == task_to_delete.get('Deadline'))):
                break

        deletion_task.pop(count - 1)
        assignedTask.pop(deletionId)
        instance.assignedTask['tasks'] = assignedTask
        deletion_instance.selfTask['tasks'] = deletion_task

        notif = deletion_instance.notification.get('notifications')
        newNotification = instance.email + " has deleted a task "+task_to_delete.get('Title')
        notif.append(newNotification)
        deletion_instance.notification['notifications'] = notif
        instance.save()
        deletion_instance.save()
        return JsonResponse({'message': 'Deleted'})
    else:
        return HttpResponse("ONLY POST REQUEST")

@csrf_exempt
def updateStatus(request):
    if (request.method == "POST"):
        updationId = (json.loads(request.body)).get('updationId')
        # updationId = 0
        instance = get_object_or_404(UserData, email=request.session.get('email'))
        selfTask=(instance.selfTask).get('tasks')

        task_to_update=selfTask[updationId]

        assigned_by_email=(selfTask[updationId]).get('AssignedBy')
        (selfTask[updationId])['Status']='Completed'

        instance.selfTask['tasks']=selfTask


        instance2=get_object_or_404(UserData,email=assigned_by_email)
        assignedTask=(instance2.assignedTask).get('tasks')

        count = 0
        for obj in assignedTask:
            count += 1
            if ((obj.get('Title') == task_to_update.get('Title')) and (
                    obj.get('Description') == task_to_update.get('Description')) and (
                    obj.get('Deadline') == task_to_update.get('Deadline'))):
                break



        (assignedTask[count-1])['Status']="Completed"

        instance2.assignedTask['tasks']=assignedTask

        instance.save()

        notif = instance2.notification.get('notifications')
        newNotification = instance.email + " has Completed the task "+task_to_update.get('Title')
        notif.append(newNotification)
        instance2.notification['notifications'] = notif
        instance2.save()
        return JsonResponse({"message":"Updated Status"})
    else:
        return HttpResponse("ONLY POST REQUEST")

@csrf_exempt
def addNotes(request):
    if request.method=="GET":
        noteDescription="Hello this is a test note 2 created by Mitesh"
        noteDate=datetime.datetime.now().date()
        instance = get_object_or_404(UserData, email=request.session.get('email'))
        notes = (instance.notes).get('notes')
        tempObj={'Description: ':noteDescription,'Date':str(noteDate)}
        notes.append(tempObj)
        instance.notes['notes']=notes
        instance.save()

        return JsonResponse({"message": "Note Addedd Successfully"})
    else:
        return HttpResponse("ONLY POST REQUEST")

@csrf_exempt
def deleteNote(request):
    deleteIndex=0
    instance=get_object_or_404(UserData,email=request.session.get('email'))
    notes=(instance.notes).get('notes')
    notes.pop(deleteIndex)
    instance.notes['notes']=notes
    instance.save()
    return JsonResponse({'message':"note Deleted"})

def updateDeadline(request):
    instance=get_object_or_404(UserData,email=request.session.get('email'))

    if request.method=="POST":
        print('post')
    else:
        return render(request,'updateDeadline.html',)