from PartyHub_Project.Party import views
from django.urls import path

urlpatterns = [
    path('all/', views.PartyListView.as_view(), name='all_parties'),
    path('live_party/<int:pk>', views.LivePartyDetailView.as_view(), name='live_party'),
    path('user_parties/', views.MyPartiesView.as_view(), name='user_parties'),
    path('create/', views.PartyCreateView.as_view(), name='create_party'),
    path('details/<int:pk>', views.PartyDetailsView.as_view(), name='details_party'),
    path('delete/<int:pk>', views.PartyDeleteView.as_view(), name='delete_party'),
]