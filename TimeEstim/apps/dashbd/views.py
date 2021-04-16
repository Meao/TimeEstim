from apps.project.models import Step
from datetime import datetime, timedelta, timezone
from dateutil.relativedelta import relativedelta
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .utilities import get_time_for_user_on_date, time_for_month, time_for_user_in_month, time_for_user_on_project_in_month, time_for_user_in_month, velocity_for_user_in_week, velocity_for_user_in_month, velocity_for_user_in_year

# Create your views here.

@login_required
def dashbd(request):
    
    # Get all projects and set variable
    us = get_object_or_404(User, pk=request.user.pk)
    all_projects = us.projects.all()

    # User date, pagination
    num_days = int(request.GET.get('num_days', 0))
    date_user = datetime.now() - timedelta(days=num_days)
    date_steps = Step.objects.filter(creator=request.user, created_at__date=date_user, is_tracked=True)
    
    # User month, pagination
    user_num_months = int(request.GET.get('user_num_months', 0))
    user_month = datetime.now()-relativedelta(months=user_num_months)
    for project in all_projects:
        project.time_user_project_month = time_for_user_on_project_in_month(project, request.user, user_month)

    # 
    untracked_steps = Step.objects.filter(creator=request.user, is_tracked=False).order_by('-created_at')
    for untracked_step in untracked_steps:
        untracked_step.minutes_since = int((datetime.now(timezone.utc) - untracked_step.created_at).total_seconds() / 60)

    # Context; 'projects': all_projects[0:4] is for the "newest projects"
    context = {
        'all_projects': all_projects,
        'date_steps': date_steps,
        'date_user': date_user,
        'num_days': num_days,
        'projects': all_projects[0:4],
        'time_user_month': time_for_user_in_month(request.user, user_month),
        'time_for_user_and_date': get_time_for_user_on_date(request.user, date_user),
        'untracked_steps': untracked_steps,
        'user_num_months': user_num_months,
        'user_month': user_month,
        'velocity_week': velocity_for_user_in_week(request.user), 
        'velocity_month': velocity_for_user_in_month(request.user), 
        'velocity_year': velocity_for_user_in_year(request.user)
    }
    return render(request, 'dashbd/dashbd.html', context)

@login_required
def view_user(request, user_id):
    # Get user and set variables
    us = get_object_or_404(User, pk=request.user.pk)
    all_projects = us.projects.all()

    # User date, pagination
    num_days = int(request.GET.get('num_days', 0))
    date_user = datetime.now() - timedelta(days=num_days)
    date_steps = Step.objects.filter(creator=request.user, created_at__date=date_user, is_tracked=True)
    
    # User month, pagination
    user_num_months = int(request.GET.get('user_num_months', 0))
    user_month = datetime.now()-relativedelta(months=user_num_months)
    for project in all_projects:
        project.time_user_project_month = time_for_user_on_project_in_month(project, request.user, user_month)
    
    # Context
    context = {
        'all_projects': all_projects,
        'date_steps': date_steps,
        'date_user': date_user,
        'num_days': num_days,
        'time_user_month': time_for_user_in_month(request.user, user_month),
        'time_for_user_and_date': get_time_for_user_on_date(request.user, date_user),
        'user_num_months': user_num_months,
        'user_month': user_month
    }
    return render(request, 'dashbd/view_user.html', context)