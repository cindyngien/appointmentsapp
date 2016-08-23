from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib import messages
from models import User, MyApp
from datetime import datetime, timedelta, time
from django.db.models import Q

def index(request):
    return render(request, 'appointments/index.html')

def register(request): #just taking the request object
    user = User.objects.register(request.POST) #user = a tuple, 2 options, (True, user) or (False, errors)
    if user[0]:
        request.session['user'] = {
            'id':user[1].id,
            'name':user[1].name,
            'email':user[1].email,
        }
        return redirect(reverse('myapp:home'))
    #build flash messages here using user[1]
    for error in user[1]: #always going to be referring as user 1 because it's the first user in the list
        messages.error(request, error)
    return redirect(reverse('myapp:index'))

def login(request):
    user = User.objects.login(request.POST)
    if user[0]:
        request.session['user'] = {
            'id':user[1].id,
            'name':user[1].name,
            'email':user[1].email,
        }
        return redirect(reverse('myapp:home')) #what this does here is when the log in is successful, it will redirect the user to the home page of the bookreview app
 #flash messages
    for error in user[1]:
        messages.error(request, error)
    return redirect(reverse('myapp:index'))

def logoff(request):
    request.session.clear()
    return redirect(reverse('myapp:index'))

def home(request):
    now = datetime.now()
    user = User.objects.get(id=request.session['user']['id'])
    context = {
        'today':datetime.now().date(),
        'todayappointment':MyApp.objects.filter(Q(my_date__lte=now, my_date__gte=now) & Q(myuser__id=user.id)).order_by('my_time'),
        'futureappointment':MyApp.objects.filter(Q(my_date__gte=now) & Q(myuser__id=user.id)).exclude(my_date__lte=now, my_date__gte=now).order_by('my_date'),
    }
    return render(request, 'appointments/appointments.html', context)

def create(request):
    result = MyApp.objects.create_app(request.POST, request.session['user']['id'])
    print result
    if result[0]:
        return redirect(reverse('myapp:home'))
    elif result[0] == False:
        errors = result[1]
        for error in errors:
            messages.error(request, error)
        return redirect(reverse('myapp:home'))
    else:
        raise ValueError("this should never happen") #this will raise an error if the 1st 2 checks are failing (but it should never happen)

def edit(request, app_id):
    context={
        'myapp':MyApp.objects.get(id=app_id)
        }
    return render(request,'appointments/edit.html', context)

def update(request, app_id):
    myapp = MyApp.objects.edit_app(request.POST)
    logged_in = User.objects.get(id=request.session['user']['id'])

    if myapp[0] == False:
        myapp = MyApp.objects.get(id=app_id)
        myapp.my_task = request.POST['task']
        myapp.my_status = request.POST['status']
        myapp.my_date = request.POST['date']
        myapp.my_time = request.POST['time']
        myapp.save()
        return redirect(reverse ('myapp:home'))
    else:
        errors = myapp[1]
        for error in errors:
                messages.error(request, error)
        return redirect(reverse ('myapp:edit', kwargs={'app_id':app_id}))

def delete(request, app_id):
    app = MyApp.objects.get(id=app_id)
    app.delete()
    return redirect(reverse('myapp:home'))
