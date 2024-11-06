from PartyHub_Project.Accounts import views
from PartyHub_Project.Accounts.views import CustomLoginView
from django.contrib.auth.views import LogoutView
from django.urls import path, include

urlpatterns = [
    path('register/', views.register, name='register'),  # за регистрация
    path('login/', CustomLoginView.as_view(), name='login'),       # за логване
    path('logout/', LogoutView.as_view(), name='logout'),    # за излизане
    path('profile/', include([
        path('details/', views.ProfileDetailsView.as_view(), name='profile_details'),
        path('edit/', views.ProfileEditView.as_view(), name='profile_edit'),
    ])),
]