from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404


from .models import Task
from task.forms import TaskForm


# Create your views here.
def home(request, sms, code, css_class):
    if code == 'TODO':
        tasks = Task.todo.all()
    elif code == 'DONE':
        tasks = Task.done.all()
    elif code == 'DELETE':
        tasks = Task.delete.all()
    elif code == 'DONE & DELETE':
        tasks = Task.done_delete.all()
    else:
        tasks = Task.objects.none()

    form = TaskForm()
    paginator = Paginator(tasks, 7)
    page_number = request.GET.get('page')
    tasks = paginator.get_page(page_number)

    context = {
        'tasks': tasks,
        'form': form,
        'sms': sms,
        'task_code': code,
        'class': css_class,
        'todo_count': Task.todo.all().count(),
        'done_count': Task.done.all().count(),
        'deleted_count': Task.delete.all().count(),
        'done_delete_count': Task.done_delete.all().count(),
        # 'search': code.lower()
    }
    return render(request, 'task/home.html', context)


@login_required
def home_view(request):
    return home(request, 'Невыполненный', 'TODO', 'warning')


@login_required
def done_task_view(request):
    return home(request, 'Выполнено', 'DONE', 'success')


@login_required
def deleted_task_view(request):
    return home(request, 'Удалено', 'DELETE', 'danger')


@login_required
def done_delete_task_view(request):
    return home(request, 'Выполнено и Удалено', 'DONE & DELETE', 'dark')


@login_required
def search(request):
    q = request.POST.get('search', '') if request.method == 'POST' else request.GET.get('search', '')

    if not q.strip():
        tasks = Task.objects.none()
    else:
        tasks = Task.objects.filter(title__icontains=q)

    tasks_count = tasks.count()
    paginator = Paginator(tasks, 7)
    page_number = request.GET.get('page')
    tasks = paginator.get_page(page_number)

    if tasks_count > 0:
        messages.success(request, f"{q} {'о' if q else ''} {tasks_count} информация найдена!")
    else:
        messages.error(request, f"{q} информация не найдена!")

    context = {
        'tasks': tasks,
        'form': TaskForm(),
        'class': 'dark',
        'sms': 'Qidirilgan',
        'todo_count': Task.todo.all().count(),
        'done_count': Task.done.all().count(),
        'deleted_count': Task.delete.all().count(),
        'done_delete_count': Task.done_delete.all().count(),
        'search': q
    }

    return render(request, 'task/home.html', context)


@login_required()
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()
            messages.success(request, f"Задание {task.title} создано!")
            return redirect('home-view')


def custom_redirect(task):
    if task.is_done and task.is_delete:
        return redirect('done-delete-task-view')
    elif task.is_delete:
        return redirect('task-delete-view')
    elif task.is_done:
        return redirect('done_task_view')
    else:
        return redirect('home-view')


@login_required()
def edit_task(request):
    if request.method == 'POST':
        task_id = request.POST['task_id']
        task = Task.objects.get(pk=task_id)
        task.title = request.POST['title']
        task.description = request.POST['description']
        task.is_done = request.POST.get('done', 'off') == 'on'
        task.is_delete = request.POST.get('delete', 'off') == 'on'
        task.save()
        messages.success(request, f"{task.title} Задание изменено!")
        # custom redirect
        return custom_redirect(task)


@login_required()
def done_task(request):
    if request.method == 'POST':
        task_id = request.POST['task_id']
        task = Task.objects.get(pk=task_id)
        task.done = True
        task.save()
        messages.success(request, f"{task.title} Задание выполнено!")
        # custom redirect
        return custom_redirect(task)


@login_required
def delete_task(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')

        if not task_id or not task_id.isdigit():
            messages.error(request, "Ошибка: ID задачи не передан.")
            return redirect('home-view')

        task = get_object_or_404(Task, pk=task_id)
        task.is_delete = True
        task.save()

        messages.success(request, f"{task.title} удалено!")
        return redirect('home-view')

    return HttpResponse(status=405)


@login_required()
def login_view(request):
    return render(request, 'login.html')


@login_required()
def logout_view(request):
    logout(request)
    return redirect('login.html')


@login_required()
def authenticate_user(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('home-view')
    else:
        messages.error(request, 'Неверный логин или пароль!')
        return redirect('login-view')


@login_required()
def register_view(request):
    return render(request, 'signup.html')


@login_required()
def profile(request):
    return render(request, 'profile.html')