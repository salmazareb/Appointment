from django.urls import path
from .import views

urlpatterns = [
    path('',views.index),
    path('process_login',views.process_login),
    path('register',views.register),
    path('process_reg',views.process_reg),
    path('success',views.success),
    path('logout',views.logout),
    path('appointments',views.appointments),
    path('add',views.add),
    path('add_process',views.add_process),
    path('edit/<int:id>',views.edit),
    path('delete/<int:id>',views.delete),
    
]