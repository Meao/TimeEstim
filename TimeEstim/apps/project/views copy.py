from apps.core.models import User
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Project, Task, Step

# Create your views here.

@login_required
def projects(request):
    us = get_object_or_404(User, pk=request.user.pk)
    projects = us.projects.all()
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            status = request.POST.get('status', 'public')
            importance = request.POST.get('importance', False)
            urgency = request.POST.get('urgency', False)
            project = Project.objects.create(title=title, creator=request.user, status=status, importance=importance, urgency=urgency)
            messages.info(request, 'Проект добавлен')
            # return redirect('project:projects')
    return render(request, 'project/projects.html', {'projects': projects})

@login_required
def project(request, project_id):
    us = get_object_or_404(User, pk=request.user.pk)
    project = get_object_or_404(Project, creator=us, pk=project_id)
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            task = Task.objects.create(project=project, creator=request.user, title=title)
            messages.info(request, 'Задача добавлена')
            return redirect('project:project', project_id=project.id)
    tasks_todo = project.tasks.filter(status=Task.TODO)
    tasks_done = project.tasks.filter(status=Task.DONE)
    return render(request, 'project/project.html', {'project': project, 'tasks_todo': tasks_todo, 'tasks_done': tasks_done})

@login_required
def edit_project(request, project_id):
    us = get_object_or_404(User, pk=request.user.pk)
    project = get_object_or_404(Project, creator=us, pk=project_id)
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            project.title = title
            project.save()
            messages.info(request, 'Изменения сохранены')
            return redirect('project:project', project_id=project.id)
    return render(request, 'project/edit_project.html', {'project': project})

@login_required
def task(request, project_id, task_id):
    us = get_object_or_404(User, pk=request.user.pk)
    project = get_object_or_404(Project, creator=us, pk=project_id)
    task = get_object_or_404(Task, creator=us, pk=task_id)
    if request.method == 'POST':
        hours = int(request.POST.get('hours', 0))
        minutes = int(request.POST.get('minutes', 0))
        date = '%s %s' % (request.POST.get('date'), datetime.now().time())
        minutes_total = (hours * 60) + minutes
        step = Step.objects.create(project=project, task=task, minutes=minutes_total, creator=request.user, created_at=date, is_tracked=True)
    context = {
        'today': datetime.today(),
        'project': project,
        'task': task,
        'h': [1, 2, 3, 5, 8], 
        'm' : list(range(5,59,5))
    }
    return render(request, 'project/task.html', context)

@login_required
def edit_task(request, project_id, task_id):
    us = get_object_or_404(User, pk=request.user.pk)
    project = get_object_or_404(Project, creator=us, pk=project_id)
    task = get_object_or_404(Task, creator=us, pk=task_id)
    if request.method == 'POST':
        title = request.POST.get('title')
        status = request.POST.get('status')
        if title:
            task.title = title
            task.status = status
            task.save()
            messages.info(request, 'Изменения сохранены')
            return redirect('project:task', project_id=project.id, task_id=task.id)
    return render(request, 'project/edit_task.html', {'project': project, 'task': task})

@login_required
def edit_step(request, project_id, task_id, step_id):
    us = get_object_or_404(User, pk=request.user.pk)
    project = get_object_or_404(Project, creator=us, pk=project_id)
    task = get_object_or_404(Task, creator=us, pk=task_id)
    step = get_object_or_404(Step, creator=us, pk=step_id)
    if request.method == 'POST':
        hours = int(request.POST.get('hours', 0))
        minutes = int(request.POST.get('minutes', 0))
        date = '%s %s' % (request.POST.get('date'), datetime.now().time())
        step.created_at = date
        step.minutes = (hours * 60) + minutes
        step.save()
        messages.info(request, 'Изменения сохранены')
        return redirect('project:task', project_id=project.id, task_id=task.id)
    hours, minutes = divmod(step.minutes, 60)
    context = {
        'project': project,
        'task': task,
        'step': step,
        'hours': hours,
        'minutes': minutes,
        'h': [1, 2, 3, 5, 8], 'm' : list(range(5,59,5))
    }
    return render(request, 'project/edit_step.html', context)

@login_required
def delete_step(request, project_id, task_id, step_id):
    us = get_object_or_404(User, pk=request.user.pk)
    project = get_object_or_404(Project, creator=us, pk=project_id)
    task = get_object_or_404(Task, creator=us, pk=task_id)
    step = get_object_or_404(Step, creator=us, pk=step_id)
    step.delete()
    messages.info(request, 'Запись удалена')
    return redirect('project:task', project_id=project.id, task_id=task.id)

# @login_required
# def delete_untracked_step(request, step_id):
#     us = get_object_or_404(User, pk=request.user.uprofile)
#     step = get_object_or_404(Step, creator=us, pk=step_id)
#     step.delete()
#     messages.info(request, 'Запись удалена')
#     return redirect('dashbd')

@login_required
def track_step(request, step_id):
    us = get_object_or_404(User, pk=request.user.pk)
    step = get_object_or_404(Step, creator=us, pk=step_id)
    projects = us.projects.all()
    if request.method == 'POST':
        # the default is 0
        hours = int(request.POST.get('hours', 0))
        minutes = int(request.POST.get('minutes', 0))
        project = request.POST.get('project')
        task = request.POST.get('task')
        if project and task:
            step.project_id = project
            step.task_id = task
            step.minutes = (hours * 60) + minutes
            step.created_at = '%s %s' % (request.POST.get('date'), step.created_at.time())
            step.is_tracked = True
            step.save()
            messages.info(request, 'Время добавлено')
            return redirect('dashbd')
    hours, minutes = divmod(step.minutes, 60)
    context = {
        'hours': hours,
        'minutes': minutes,
        'projects': projects,
        'step': step,
        'h': list(range(1,23)), 
        'm': list(range(1,59))
    }
    return render(request, 'project/track_step.html', context)