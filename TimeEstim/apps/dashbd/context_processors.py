from apps.project.models import Step
from datetime import datetime, timezone
from django.shortcuts import get_object_or_404


def active_step(request):
    if request.user.is_authenticated:
        untracked_steps = Step.objects.filter(creator=request.user, minutes=0, is_tracked=False)
        if untracked_steps:
            active_step = untracked_steps.first()
            active_step.seconds_since = int((datetime.now(timezone.utc) - active_step.created_at).total_seconds())
            # isoformat for milliseconds
            return {'active_step_seconds': active_step.seconds_since, 'start_time': active_step.created_at.isoformat()}
    return {'active_step_seconds': 0, 'start_time': datetime.now().isoformat()}