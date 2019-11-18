from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import DetailView

from tasker.forms import UserSettingForm, UserCreateForm
from tasker.managers import UserManager, ProjectManager
from tasker.models import Project


@login_required
def profile_view(request, slug=None):
    if request.method == 'GET':
        if slug:
            user = UserManager.safe_get(slug__iexact=slug.lower())
            projects = user.get_all_projects()
            return render(request, 'profile/profile_page.html',
                          context={'user': user, 'projects': projects, 'request_user': request.user})
        else:
            projects = request.user.get_all_projects()
            return render(request, 'profile/profile_page.html',
                          context={'user': request.user, 'projects': projects, 'request_user': request.user})


@login_required
def profile_settings_view(request):
    form_change_password = PasswordChangeForm(user=request.user, data=request.POST or None)
    if request.method == "GET":
        form = UserSettingForm(instance=request.user)
        return render(request, 'profile/profile_settings.html', context={'user': request.user, 'form': form,
                                                                         'password_form': form_change_password})
    elif request.method == "POST" and "category" in request.POST:
        if request.POST['category'] == 'info_change':
            form = UserSettingForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                return redirect('profile_url')
            return render(request, 'profile/profile_settings.html', context={'user': request.user, 'form': form,
                                                                             'password_form': form_change_password})
        elif request.POST['category'] == 'pass_change':
            if form_change_password.is_valid():
                form_change_password.save()
                return redirect('profile_url')
            form = UserSettingForm(request.POST, instance=request.user)
            return render(request, 'profile/profile_settings.html', context={'user': request.user, 'form': form,
                                                                             'password_form': form_change_password})


def create_user_view(request):
    form = UserCreateForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        user.save()
        return redirect('profile_url', slug=user.username)
    return render(request, 'models_actions/user/user_create.html', context={'form': form, 'model_type': 'User'})


@login_required
def projects_view(request):
    projects = ProjectManager.get_queryset()
    return render(request, 'projects/projects_page.html', context={'projects': projects})


class DetailsProjectView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'models_actions/project/project_details.html'
