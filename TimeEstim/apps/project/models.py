from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models


from .forms import  DateInput
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from bulma_widget import widgets
# Create your models here.

def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]

class Project(models.Model):
    PUBLIC = 'public'
    PRIVATE = 'private'
    CHOICES_STATUS = (
        (PUBLIC, 'Публичный'),
        (PRIVATE, 'Закрытый')
    )
    title = models.CharField(max_length=255)
    creator = models.ForeignKey(User, related_name='projects', on_delete=models.SET(get_sentinel_user))
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=CHOICES_STATUS, default=PUBLIC)
    importance = models.BooleanField(default=False)
    urgency = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        # ordering = ['title']
    # string representation
    def __str__(self):
        return self.title
    
    def registered_time(self):
        return sum(step.minutes for step in self.steps.all())
    
    def num_tasks_todo(self):
        return self.tasks.filter(status=Task.TODO).count()
    
    def num_tasks_ongoing(self):
        return self.tasks.filter(status=Task.ONGOING).count()
    
    def num_tasks_testing(self):
        return self.tasks.filter(status=Task.TESTING).count()

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'status', 'importance', 'urgency']
        labels = {
            'title': _('Название'),
            'status': _('Статус'),
            'importance': _('Важный'),
            'urgency': _('Срочный'),
        }

class Task(models.Model):
    class ScrumPocker(models.IntegerChoices):
        O = 1, _('1')
        T = 2, _('2')
        TH = 3, _('3')
        F = 5, _('5')
        E = 8, _('8')
    TODO = 'todo'
    ONGOING = 'ongoing'
    TESTING = 'testing'
    DONE = 'done'
    ARCHIVED = 'archived'
    CHOICES_STATUS = (
        (TODO, 'Сделать'),
        (ONGOING, 'В процессе'),
        (TESTING, 'Тестируется'),
        (DONE, 'Сделано'),
        (ARCHIVED, 'В архиве')
    )
    project = models.ForeignKey(Project, related_name='tasks', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    aim = models.CharField(max_length=255, blank = True, null=True, default=None)
    due_date = models.DateTimeField(blank = True, null=True, default=None)
    estimated_length = models.IntegerField(choices=ScrumPocker.choices, default=1)
    responsible_role = models.CharField(max_length=255, blank = True, null=True, default=None)
    resources = models.CharField(max_length=255, blank = True, null=True, default=None)
    creator = models.ForeignKey(User, related_name='tasks', on_delete=models.SET(get_sentinel_user))
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=CHOICES_STATUS, default=TODO)
    source = models.CharField(max_length=255, blank = True, null=True, default=None)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def registered_time(self):
        return sum(step.minutes for step in self.steps.all())

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'aim', 'due_date', 'estimated_length', 'responsible_role', 'resources', 'status']
        labels = {
            'title': _('Название'),
            'aim': _('Цель'),
            'due_date': _('Дедлайн'),
            'estimated_length': _('Расчетное время'),
            'responsible_role': _('Отдел / роль'),
            'resources': _('Ресурсы'),
            'status': _('Статус'),
        }
        widgets = {
            'due_date': DateInput(format=('%d/%m/%Y'), attrs={'class':'input', 'placeholder':'Выбор даты', 'type':'date'}),
        }

class Step(models.Model):
    project = models.ForeignKey(Project, related_name='steps', on_delete=models.CASCADE, blank=True, null=True)
    task = models.ForeignKey(Task, related_name='steps', on_delete=models.CASCADE, blank=True, null=True)
    minutes = models.IntegerField(default=0)
    is_tracked = models.BooleanField(default=False)
    creator = models.ForeignKey(User, related_name='steps', on_delete=models.CASCADE)
    created_at = models.DateTimeField()

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        if self.task:
            return '%s - %s' % (self.task.title, self.created_at)
        return '%s' % self.created_at