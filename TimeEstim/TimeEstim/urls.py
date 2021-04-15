"""TimeEstim URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
# from apps.bot.views import ChatterBotAppView, ChatterBotApiView
from apps.bot.views import ChatterBotAppView
from apps.bot.api import ChatterBotView
from apps.core.views import index, plans, profile, signup, templates
from apps.dashbd.api import api_start_timer, api_stop_timer, api_discard_timer, api_get_tasks
from apps.dashbd.views import dashbd
from apps.project.views import project, projects, edit_project, delete_project, task, edit_task, delete_task, edit_step, delete_step, track_step, delete_untracked_step

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', index, name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('plans/', plans, name='plans'),
    path('accounts/profile/', profile, name='profile'),
    path('signup/', signup, name='signup'),
    path('templates/', templates, name='templates'),

    path('api/start_timer/', api_start_timer, name='api_start_timer'),
    path('api/stop_timer/', api_stop_timer, name='api_stop_timer'),
    path('api/discard_timer/', api_discard_timer, name='api_discard_timer'),
    path('api/get_tasks/', api_get_tasks, name='api_get_tasks'),
    path('delete_untracked_step/<int:step_id>/', delete_untracked_step, name='delete_untracked_step'),
    path('<int:project_id>/', project, name='project'),
    path('<int:project_id>/delete/', delete_project, name='delete_project'),
    path('<int:project_id>/<int:task_id>/', task, name='task'),
    path('<int:project_id>/<int:task_id>/edit/', edit_task, name='edit_task'),
    path('<int:project_id>/<int:task_id>/delete/', delete_task, name='delete_task'),
    path('<int:project_id>/<int:task_id>/<int:step_id>/edit/', edit_step, name='edit_step'),
    path('<int:project_id>/<int:task_id>/<int:step_id>/delete/', delete_step, name='delete_step'),
    path('<int:project_id>/edit/', edit_project, name='edit_project'),
    path('track_step/<int:step_id>/', track_step, name='track_step'),
    path('projects/', projects, name='projects'),
    path('dashbd/', dashbd, name='dashbd'),
    url(r'^postbot/', ChatterBotView.as_view(), name='chatterbot'),
    url(r'^bot/', ChatterBotAppView.as_view(), name='bot'),
    # url(r'^admin/', admin.site.urls, name='admin'),
    # url(r'^api/chatterbot/', ChatterBotApiView.as_view(), name='chatterbot'),
]
if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)