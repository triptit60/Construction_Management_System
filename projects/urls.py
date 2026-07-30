from django.urls import path
from . import views

urlpatterns = [
    #proects urls
    path('projects/', views.project_list, name='project_list'),
    path('projects/create/', views.project_create, name='project_create'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
    path('projects/<int:pk>/update/', views.project_update, name='project_update'),
    path('projects/<int:pk>/delete/', views.project_delete, name='project_delete'),
    path("projects/<int:pk>/dashboard/",views.project_dashboard,name="project_dashboard"),

    #Task Urls
    # Task URLs
     path("projects/<int:project_id>/tasks/",views.task_list,name="task_list",),
     path("projects/<int:project_id>/tasks/create/",views.task_create,name="task_create",),
     path("projects/<int:project_id>/tasks/<int:pk>/",views.task_detail,name="task_detail",),
     path("projects/<int:project_id>/tasks/<int:pk>/update/",views.task_update,name="task_update",),
     path("projects/<int:project_id>/tasks/<int:pk>/delete/",views.task_delete,name="task_delete",),
]