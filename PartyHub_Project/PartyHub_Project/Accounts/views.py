from PartyHub_Project.Accounts.forms import UserProfileCreateForm
from PartyHub_Project.Accounts.models import UserProfile
from django.contrib.auth import login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, UpdateView, CreateView, ListView


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserProfileCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.backend = 'PartyHub_Project.Accounts.authentication.EmailOrUsernameBackend'
            user.save()
            login(request, user)  # автоматично влизане след регистрация
            # messages.success(request, 'Registered successfully!')
            return redirect('profile_details')  # пренасочване към профила на потребителя
    else:
        form = UserProfileCreateForm()
    return render(request, 'Accounts/register.html', {'form': form})

# class RegisterView(CreateView):
#     form_class = UserProfileCreateForm
#     template_name = 'Accounts/register.html'
#     success_url = reverse_lazy('profile_details')  # Пренасочване след успешна регистрация
#
#     def form_valid(self, form):
#         user = form.save(commit=False)
#         user.backend = 'PartyHub_Project.Accounts.authentication.EmailOrUsernameBackend'
#         response = super().form_valid(form)
#         user = self.object
#         login(self.request, user)  # Логване на потребителя след регистрация
#         return response  # Връща успешен отговор потребител




class ProfileDetailsView(LoginRequiredMixin, DetailView):
    template_name = 'accounts/profile_details.html'
    context_object_name = 'user'

    def get_object(self):
        return self.request.user


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    template_name = 'Accounts/profile_edit.html'
    success_url = reverse_lazy('profile_details')
    fields = ['profile_picture', 'bio', 'first_name', 'last_name']


    def get_object(self):
        return self.request.user  #TODO: fix the view to edit username too


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"

    def get_success_url(self):
        return reverse_lazy('profile_details')


class ShowFollowingView(LoginRequiredMixin, ListView):
    model = UserProfile
    template_name = 'Accounts/following_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        following_list = self.request.user.get_following()
        context = {
            'following_list': following_list
        }
        # print(friends_list)
        return super().get_context_data(**context)


class UsersListView(ListView):
    model = UserProfile
    template_name = 'Accounts/Users_search.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        # print(self.request.user)#// TODO:Make it work with search form
        users_list = self.request.user.get_users_not_in_followers()
        print(users_list)
        context = {
            'users': users_list
        }
        return super().get_context_data(**context)

class AddFollowView(LoginRequiredMixin,     View):
    def post(self, request, *args, **kwargs):
        other = get_object_or_404(UserProfile, pk=kwargs.get('pk'))
        self.request.user.follow(other)
        return redirect('users')

class RemoveFollowView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        other = get_object_or_404(UserProfile, pk=kwargs.get('pk'))
        self.request.user.unfollow(other)
        return redirect('following_list')


class UsersDetailView(DetailView):
    model = UserProfile
    template_name = 'Accounts/user_details.html'

class ShowFollowersView(LoginRequiredMixin, ListView):
    model = UserProfile
    template_name = 'Accounts/followers_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        users_list = self.request.user.get_followers()
        print(users_list.first().user.username)
        context = {
            'followers_list': users_list
        }
        return super().get_context_data(**context)