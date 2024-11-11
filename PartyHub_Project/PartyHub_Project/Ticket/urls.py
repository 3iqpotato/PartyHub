from PartyHub_Project.Ticket import views
from django.urls import path

urlpatterns = [
    path('user_tickets/<int:pk>/', views.UserTicketsListView.as_view(), name='user_tickets'),
    path('get_ticket/<slug:party_slug>/', views.TicketCreateView.as_view(), name='get_ticket'),
    path('delete_ticket/<int:pk>/', views.TicketDeleteView.as_view(), name='delete_ticket'),
    path('party_ticket_detail/<int:pk>/', views.TicketDetailsView.as_view(), name='party_ticket_detail'),
    path('mark_as_arrived/<int:pk>/', views.MarkAsArrivedView.as_view(), name='mark_as_arrived'),
    path('mark_as_not_arrived/<int:pk>/', views.MarkAsNotArrivedView.as_view(), name='mark_as_not_arrived'),
]