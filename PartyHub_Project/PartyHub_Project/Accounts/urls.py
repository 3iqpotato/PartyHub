from PartyHub_Project.Accounts import views
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include

urlpatterns = [
    path('register/', views.register, name='register'),  # за регистрация
    path('login/', LoginView.as_view(template_name="accounts/login.html"), name='login'),       # за логване
    path('logout/', LogoutView.as_view(), name='logout'),    # за излизане
    # path('profile/', views.ProfileDetailsView.as_view(), name='profile'),
    path('profile/', include([
        path('details/', views.ProfileDetailsView.as_view(), name='profile_details'),
        path('edit/', views.ProfileEditView.as_view(), name='profile_edit'),
    ])),
]