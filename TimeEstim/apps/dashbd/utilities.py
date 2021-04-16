from apps.project.models import Step, Task
from datetime import datetime
from dateutil.relativedelta import relativedelta


def get_time_for_user_on_date(user, date):
    steps = Step.objects.filter(creator=user, created_at__date=date, is_tracked=True)
    return sum(step.minutes for step in steps)

def time_for_user_in_month(user, month):
    steps = Step.objects.filter(creator=user, created_at__year=month.year, created_at__month=month.month, is_tracked=True)
    return sum(step.minutes for step in steps)

def time_for_user_on_project_in_month(project, user, month):
    steps = Step.objects.filter(project=project, creator=user, created_at__year=month.year, created_at__month=month.month, is_tracked=True)
    return sum(step.minutes for step in steps)

def time_for_month(month):
    steps = Step.objects.filter(created_at__year=month.year, created_at__month=month.month, is_tracked=True)
    return sum(step.minutes for step in steps)

def velocity_for_user_in_week(user):
    week = datetime.today() - relativedelta(days=7)
    tasks = Task.objects.filter(creator=user, done_date__gte=week)
    return sum(task.estimated_length for task in tasks)

def velocity_for_user_in_month(user):
    month = datetime.now() - relativedelta(months=1)
    tasks = Task.objects.filter(creator=user, done_date__gte=month)
    # tasks = Task.objects.filter(creator=user, done_date__year=month.year, done_date__month=month.month)
    return sum(task.estimated_length for task in tasks)

def velocity_for_user_in_year(user):
    year = datetime.now() - relativedelta(years=1)
    tasks = Task.objects.filter(creator=user, done_date__gte=year)
    # tasks = Task.objects.filter(creator=user, done_date__year=year.year)
    return sum(task.estimated_length for task in tasks)
