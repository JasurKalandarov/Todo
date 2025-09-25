from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home-view'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),

    path('create-task/', views.create_task, name='create_task'),
    path('edit-task/', views.edit_task, name='edit-task'),
    path('delete-task/', views.delete_task, name='delete-task'),

    path('done-task/', views.done_task_view, name='done_task_view'),
    path('deleted-task/', views.deleted_task_view, name='task-delete-view'),
    path('done-deleted-task/', views.done_delete_task_view, name='done-delete-task-view'),

    path('search/', views.search, name='search-task'),
    path('profile/', views.profile,  name='profile')

]
