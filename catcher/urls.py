from django.urls import path
from . import views

urlpatterns = [    
    path('rdstation_webhook/', views.rdstationWebhook, name='rds webhook'),
    path('pipedrive_webhook/', views.pipedriveWebhook, name='pipe webhook'),
    path('log/', views.LogList.as_view()),     
]