from PartyHub_Project.Accounts import views
from django.contrib.auth.views import LogoutView
from django.urls import path, include

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),  # за регистрация
    path('login/', views.CustomLoginView.as_view(), name='login'),       # за логване
    path('logout/', LogoutView.as_view(), name='logout'),    # за излизане
    path('users/', views.UsersListView.as_view(), name='users'),    # за излизане
    path('users/<int:pk>', views.UsersDetailView.as_view(), name='user_details'),    # за излизане
    path('profile/', include([
        path('details/<int:pk>', views.ProfileDetailsView.as_view(), name='profile_details'),
        path('edit/<int:pk>', views.ProfileEditView.as_view(), name='profile_edit'),
        path('following/<int:pk>', views.ShowFollowingView.as_view(), name='following_list'),
        path('followers/<int:pk>', views.ShowFollowersView.as_view(), name='followers_list'),
        path('following/add/<int:pk>', views.AddFollowView.as_view(), name='follow'),
        path('following/remove/<int:pk>', views.RemoveFollowView.as_view(), name='unfollow'),
    ])),
]