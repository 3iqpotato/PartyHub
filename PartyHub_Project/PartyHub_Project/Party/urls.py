from PartyHub_Project.Party import views
from django.urls import path

urlpatterns = [
    path('all/', views.PartyListView.as_view(), name='all_parties'),
]