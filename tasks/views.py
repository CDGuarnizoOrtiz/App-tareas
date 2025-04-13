from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import tasksform
from .models import tasks
from django.utils import timezone
from django.contrib.auth.decorators import login_required


# Create your views here.


def home(request):
    return render(request, 'home.html')


def signup(request):

    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })

    else:
        if request.POST['password1'] == request.POST['password2']:
            # registeruser
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'User alreay exist'
                })

        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'passwor do not match'
        })

@login_required
def tasks_(request):
    task_list = tasks.objects.filter(user=request.user, datecompleted__isnull=True)  # Solo tareas sin completar
    return render(request, 'tasks.html', {
        'tasks': task_list
    })
    
@login_required
def tasks_completed(request):
    task_list = tasks.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')  # Solo tareas sin completar
    return render(request, 'tasks.html', {
        'tasks': task_list
    })

@login_required
def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'username o password is incorrect'
            })
        else:
            login(request, user)
            return redirect('tasks')

@login_required
def create_tasks(request):

    if request.method == 'GET':
        return render(request, 'create_tasks.html', {
            'form': tasksform
        })
    else:
        try:
            form = tasksform(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_tasks.html', {
                'form': tasksform,
                'error': 'please provide valide data'
            })

@login_required
def task_detail(request, tasks_id):
    if request.method == 'GET':
        task = get_object_or_404(tasks, pk=tasks_id,user=request.user)
        form = tasksform(instance=task)

        return render(request, 'task_detail.html', {
            'task': task,
            'form': form
        })
    else:
        try:
            task = get_object_or_404(tasks, pk=tasks_id,user=request.user)
            form = tasksform(request.POST,instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
             return render(request, 'task_detail.html', {
            'task': task,
            'form': form,
            'error': "Error updating task"
        })
            
@login_required      
def complete_task(request, tasks_id):
    task = get_object_or_404(tasks, pk=tasks_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()  
        task.save()
        return redirect('tasks')  

@login_required
def delete_task(request, tasks_id):
    task = get_object_or_404(tasks, pk=tasks_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks') 