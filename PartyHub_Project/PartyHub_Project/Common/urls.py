from PartyHub_Project.Common import views
from django.urls import path

urlpatterns = [
    path('', views.indexview, name='index'),
]