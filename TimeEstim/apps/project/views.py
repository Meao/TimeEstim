from apps.core.models import User
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Project, Task, Step, ProjectForm, TaskForm

# Create your views here.

@login_required
def projects(request):
    us = get_object_or_404(User, pk=request.user.pk)
    projects = us.projects.all()
    if request.method == 'POST':
        project = Project.objects.create(creator=request.user)
        form = ProjectForm(request.POST, instance=project)
        form.save()
        messages.info(request, 'Проект добавлен')
        return redirect('projects')
    else:
        form = ProjectForm()
    return render(request, 'project/projects.html', {'form': form, 'projects': projects})

@login_required
def project(request, project_id):
    us = get_object_or_404(User, pk=request.user.pk)
    project = get_object_or_404(Project, creator=us, pk=project_id)
    if request.method == 'POST':
        task = Task.objects.create(project=project, creator=request.user)
        form = TaskForm(request.POST, instance=task)
        form.save()
        messages.info(request, 'Задача добавлена')
        return redirect('project', project_id=project.id)
    else:
        form = TaskForm()
    tasks_todo = project.tasks.filter(status=Task.TODO)
    tasks_ongoing = project.tasks.filter(status=Task.ONGOING)
    tasks_testing = project.tasks.filter(status=Task.TESTING)
    tasks_done = project.tasks.filter(status=Task.DONE)
    tasks_archived = project.tasks.filter(status=Task.ARCHIVED)
    context = {
        'form': form, 
        'project': project, 
        'tasks_todo': tasks_todo, 
        'tasks_ongoing': tasks_ongoing,
        'tasks_testing': tasks_testing,
        'tasks_done': tasks_done,
        'tasks_archived': tasks_archived
    }
    return render(request, 'project/project.html', context)

@login_required
def edit_project(request, project_id):
    us = get_object_or_404(User, pk=request.user.pk)
    project = get_object_or_404(Project, creator=us, pk=project_id)
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            status = request.POST.get('status')
            importance = request.POST.get('importance')
            urgency = request.POST.get('urgency')
            project.title = title
            project.status = status
            project.importance = importance
            project.urgency = urgency
            project.save()
            messages.info(request, 'Изменения сохранены')
            return redirect('project', project_id=project.id)
    return render(request, 'project/edit_project.html', {'project': project})

@login_required
def delete_project(request, project_id):
    us = get_object_or_404(User, pk=request.user.pk)
    project = get_object_or_404(Project, creator=us, pk=project_id)
    project.delete()
    messages.info(request, 'Проект удален')
    return redirect('projects')

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
        aim = request.POST.get('aim')
        due_date = request.POST.get('due_date')
        estimated_length = int(request.POST.get('estimated_length'))
        responsible_role = request.POST.get('responsible_role')
        resources = request.POST.get('resources')
        status = request.POST.get('status')
        if title:
            task.title = title
            task.aim = aim
            task.due_date = due_date
            task.estimated_length = estimated_length
            task.responsible_role = responsible_role
            task.resources = resources
            if status == 'done':
                # done_date = datetime.now().time()
                # print(done_date)
                # done_date = datetime.now()
                # print(done_date)
                # done_date = datetime.now().date()
                # print(done_date)
                task.done_date = datetime.now().date()
            else:
                task.done_date = None
                # done_date = None
                # print(done_date)
            # print(status)
            task.status = status
            task.save()
            messages.info(request, 'Изменения сохранены')
            return redirect('task', project_id=project.id, task_id=task.id)
    return render(request, 'project/edit_task.html', {'project': project, 'task': task})

@login_required
def delete_task(request, project_id, task_id):
    us = get_object_or_404(User, pk=request.user.pk)
    project = get_object_or_404(Project, creator=us, pk=project_id)
    task = get_object_or_404(Task, creator=us, pk=task_id)
    task.delete()
    messages.info(request, 'Задача удалена')
    return redirect('project', project_id=project.id)

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
        return redirect('task', project_id=project.id, task_id=task.id)
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
    messages.info(request, 'Время удалено')
    return redirect('task', project_id=project.id, task_id=task.id)

@login_required
def delete_untracked_step(request, step_id):
    us = get_object_or_404(User, pk=request.user.pk)
    step = get_object_or_404(Step, creator=us, pk=step_id)
    step.delete()
    messages.info(request, 'Время удалено')
    return redirect('dashbd')

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