from apps.project.models import Step
from datetime import datetime


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