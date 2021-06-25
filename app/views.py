from django.shortcuts import render, redirect
from .models import User,Task
from django.contrib import messages
import bcrypt  

# Create your views here.
def index(request):
    return render(request, 'index.html')

def process_login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, val in errors.items():
            messages.error(request, val)
        return redirect('/')
    else:
        user = User.objects.get(email=request.POST['email'])
        request.session['logged_in'] = user.id 
        return redirect('/success')


def register(request):
    return render(request, 'register.html')

def process_reg(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, val in errors.items():
            messages.error(request, val)
        return redirect('/register')
    else:
        uname = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        pwd_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode() # create the hash
        user = User.objects.create(username=uname, email=email, password=pwd_hash)
        request.session['logged_in'] = user.id 
        return redirect('/success')


def success(request):
    context = {
        "logged_in" : User.objects.get(id=request.session['logged_in']),
    }
    return render(request, 'success.html', context)
    

def logout(request):
    return redirect('/')


def appointments(request):
    context = {
        "tasks" : Task.objects.all()
    }
    return render(request, 'appointments.html', context)

def add(request):
    return render(request, 'add.html')

def add_process(request):
    errors = Task.objects.task_validator(request.POST)
    if len(errors) > 0:
        for key, val in errors.items():
            messages.error(request, val)
        return redirect('/add')
    else:
        task = request.POST['task']
        status = request.POST['status']
        date = request.POST['date']
        task = Task.objects.create(task=task, status=status, date=date)
        request.session['logged_in'] = task.id 
        return redirect('/appointments')

def edit(request,id):
    errors = Task.objects.task_validator(request.POST)
    if len(errors) > 0:
        for key, val in errors.items():
            messages.error(request, val)
        return redirect('/edit')
    else:
        task = request.POST['task']
        status = request.POST['status']
        date = request.POST['date']
        task = Task.objects.get(id=id)
        task.task = task 
        task.date = date
        task.status = status
        task.save() 
        return redirect('/appointments')

def delete(request,id):
    task_id=Task.objects.get(id=id)
    task_id.delete()

    return redirect('/appointments')


