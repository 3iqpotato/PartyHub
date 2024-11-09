from PartyHub_Project.Accounts.forms import UserProfileCreateForm, UserProfileLoginForm
from django.contrib.auth import login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, UpdateView, CreateView, ListView

UserModel = get_user_model()
# Create your views here.
# def register(request):
#     if request.method == 'POST':
#         form = UserProfileCreateForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.backend = 'PartyHub_Project.Accounts.authentication.EmailOrUsernameBackend'
#             user.save()
#             login(request, user)  # автоматично влизане след регистрация
#             # messages.success(request, 'Registered successfully!')
#             return redirect('profile_details')  # пренасочване към профила на потребителя
#     else:
#         form = UserProfileCreateForm()
#     return render(request, 'Accounts/register.html', {'form': form})

class RegisterView(CreateView):
    form_class = UserProfileCreateForm
    template_name = 'Accounts/register.html'
     # Пренасочване след успешна регистрация

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(self.request, user)  # Логване на потребителя след регистрация
        return response  # Връща успешен отговор потребител

    def get_success_url(self):
        return reverse_lazy('profile_details', kwargs={'pk': self.object.pk})


class ProfileDetailsView(LoginRequiredMixin, DetailView):
    model = UserModel
    template_name = 'accounts/profile_details.html'
    context_object_name = 'user'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     live_party = self.request.user.get_live_party()
    #     context.update({'live_party': live_party})
    #     return context


class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = UserModel
    template_name = 'Accounts/profile_edit.html'
    fields = ['profile_picture', 'bio', 'first_name', 'last_name', 'username']

    def test_func(self):
        profile = get_object_or_404(UserModel, pk=self.kwargs['pk'])
        return self.request.user == profile

    def get_success_url(self):
        return reverse_lazy('profile_details', kwargs={'pk': self.request.user.pk})
                                                                     #TODO: fix the view to edit username too


class CustomLoginView(LoginView):
    model = UserModel
    template_name = "accounts/login.html"
    form_class = UserProfileLoginForm

    def get_success_url(self):
        return reverse_lazy('profile_details', kwargs={'pk': self.request.user.pk})


class ShowFollowingView(LoginRequiredMixin,UserPassesTestMixin, ListView):
    model = UserModel
    template_name = 'Accounts/following_list.html'

    def test_func(self):
        profile = get_object_or_404(UserModel, pk=self.kwargs['pk'])
        return self.request.user == profile

    def get_context_data(self, *, object_list=None, **kwargs):
        following_list = self.request.user.get_following()
        context = {
            'following_list': following_list
        }
        return super().get_context_data(**context)


class UsersListView(ListView):
    model = UserModel
    template_name = 'Accounts/Users_search.html'

    def get_context_data(self, *, object_list=None, **kwargs):
                                                        #// TODO:Make it work with search form
        users_list = self.request.user.get_users_not_in_followers()

        query = self.request.GET.get('query', '')

        if query:
            users_list = users_list.filter(username__icontains=query)

        context = {
            'users': users_list
        }
        return super().get_context_data(**context)


class AddFollowView(LoginRequiredMixin, View):

    # def test_func(self):
    #     profile = get_object_or_404(UserModel, pk=self.kwargs['pk'])
    #     return self.request.user == profile

    def post(self, request, *args, **kwargs):

        other = get_object_or_404(UserModel, pk=kwargs.get('pk'))
        self.request.user.follow(other)
        return redirect(request.META.get('HTTP_REFERER'))

class RemoveFollowView(LoginRequiredMixin, View):

    # def test_func(self):
    #     profile = get_object_or_404(UserModel, pk=self.kwargs['pk'])
    #     return self.request.user == profile

    def post(self, request, *args, **kwargs):
        other = get_object_or_404(UserModel, pk=kwargs.get('pk'))
        self.request.user.unfollow(other)
        return redirect('following_list', self.request.user.pk)


class UsersDetailView(DetailView):
    model = UserModel
    template_name = 'Accounts/user_details.html'
    context_object_name = 'other_user'



class ShowFollowersView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = UserModel
    template_name = 'Accounts/followers_list.html'

    def test_func(self):
        profile = get_object_or_404(UserModel, pk=self.kwargs['pk'])
        return self.request.user == profile

    def get_context_data(self, *, object_list=None, **kwargs):
        user = self.request.user
        following_followers = user.get_followers().filter(following__in=[user])

        non_following_followers = user.get_followers().exclude(following__in=[user])

        context = {
            'user': user,
            'following_followers': following_followers,
            'non_following_followers': non_following_followers,
        }
        # users_list = self.request.user.get_followers()
        # context = {
        #     'followers_list': users_list
        # }
        return super().get_context_data(**context)