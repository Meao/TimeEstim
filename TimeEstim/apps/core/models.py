from django.contrib.auth.models import User
from django.db import models

class Userprofile(models.Model):
    user = models.OneToOneField(User, related_name='uprofile', on_delete=models.CASCADE)
    # velocity = models.IntegerField(default=0)
