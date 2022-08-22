from django.urls import path
from . import views

urlpatterns = [    
    path('addUpdatePerson/', views.addUpdatePerson, name='add or update a person'),    
]