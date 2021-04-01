from  datetime import datetime, timezone
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import json
from apps.project.models import Project, Step


def api_start_timer(request):
    # print(request.user)
    # print(datetime.now())
    step = Step.objects.create(
        minutes=0,
        creator=request.user,
        is_tracked=False,
        created_at=datetime.now()
    )
    # print(step)
    return JsonResponse({'success': True})

def api_stop_timer(request):
    step = Step.objects.get(
        creator=request.user,
        minutes=0,
        is_tracked=False
    )
    tracked_minutes = int((datetime.now(timezone.utc) - step.created_at).total_seconds() / 60)
    if tracked_minutes < 1:
        tracked_minutes = 1
    step.minutes = tracked_minutes
    step.is_tracked = False
    step.save()
    # print('stepID', step.id)
    return JsonResponse({'success': True, 'stepID': step.id})

def api_discard_timer(request):
    steps = Step.objects.filter(creator=request.user, is_tracked=False).order_by('-created_at')
    if steps:
        step = steps.first()
        step.delete()
    return JsonResponse({'success': True})

def api_get_tasks(request):
    # Getting the project id from the url parameter
    project_id = request.GET.get('project_id', '')
    if project_id:
        tasks = []
        # print('request.user', request.user)
        # to only get proj from this user
        project = get_object_or_404(Project, pk=project_id)
        for task in project.tasks.all():
            obj = {
                'id': task.id,
                'title': task.title
            }
            tasks.append(obj)
        return JsonResponse({'success': True, 'tasks': tasks})
    return JsonResponse({'success': False})