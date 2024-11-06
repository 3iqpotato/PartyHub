from PartyHub_Project.Accounts import views
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

urlpatterns = [
    path('register/', views.register, name='register'),  # за регистрация
    path('login/', LoginView.as_view(), name='login'),       # за логване
    path('logout/', LogoutView.as_view(), name='logout'),    # за излизане
    # path('profile/', views.profile, name='profile'),      # за профил (опционално)
]