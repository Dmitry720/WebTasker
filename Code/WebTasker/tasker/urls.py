from django.urls import path
from . import views

urlpatterns = [
    # BASE
    path('', main_url, name='main_url'),

    # USERS
    path('create-user/', views.create_user_view, name='create_user_url'),
    path('profile/', views.profile_view, name='profile_url'),
    path('profile/<slug>/', views.profile_view, name='profile_user_url'),
    path('profile-settings/', views.profile_settings_view, name='profile_settings_url'),

    # PROJECTS
    path('project-list/', views.projects_view, name='projects_url'),
    path('project/<slug>/', views.DetailsProjectView.as_view(), name='project_details_url'),

    # TASK
    path('task/<slug>/', views.DetailsTaskView.as_view(), name='task_details_url'),
    path('create-task/', views.CreateTaskView.as_view(), name='create_task_url'),
    path('edit-task/<slug>/', views.EditTaskView.as_view(), name='edit_task_url'),
    path('mark-completed-task/<slug>/', views.mark_task_is_completed_view, name='mark_task_complete'),
    path('mark-canceled-task/<slug>/', views.mark_task_is_canceled_view, name='mark_task_canceled'),

    # AUTH
    path('login/', user_login_url, name='user_login_url', kwargs={'redirect_authenticated_user': True}),
    path('logout/', user_logout_url, name='user_logout_url'),

    # DELETING
    path('delete-task/<slug>/', delete_task, name='delete_task'),
]
