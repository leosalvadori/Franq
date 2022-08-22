from django.urls import path
from . import views

urlpatterns = [    
    path('authlisttoken/', views.AuthList.as_view()),
    path('addUpdateDeleteContact/', views.addUpdateDeleteContact, name='add, update or delete a contact'),
]