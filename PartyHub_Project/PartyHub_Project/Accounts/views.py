from PartyHub_Project.Accounts.forms import UserProfileCreateForm, UserProfileLoginForm, UserProfileEditForm
from PartyHub_Project.Accounts.models import FollowTable
from django.contrib.auth import login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, UpdateView, CreateView, ListView

UserModel = get_user_model()


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


class ProfileDetailsView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = UserModel
    template_name = 'accounts/profile_details.html'
    context_object_name = 'user'

    def test_func(self):
        profile = get_object_or_404(UserModel, pk=self.kwargs['pk'])
        return self.request.user == profile


class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = UserModel
    template_name = 'Accounts/profile_edit.html'
    form_class = UserProfileEditForm

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


class ShowFollowingView(LoginRequiredMixin, UserPassesTestMixin, ListView):
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

        users_list = self.request.user.get_users_not_in_followers()

        query = self.request.GET.get('query', '')

        if query:
            users_list = users_list.filter(username__icontains=query)

        context = {
            'users': users_list
        }
        return super().get_context_data(**context)


class AddFollowView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):

        other = get_object_or_404(UserModel, pk=kwargs.get('pk'))
        self.request.user.follow(other)
        return redirect(request.META.get('HTTP_REFERER'))

class RemoveFollowView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        other = get_object_or_404(UserModel, pk=kwargs.get('pk'))
        self.request.user.unfollow(other)
        return redirect(request.META.get('HTTP_REFERER'))


class UsersDetailView(DetailView):
    model = UserModel
    template_name = 'Accounts/user_details.html'
    context_object_name = 'other_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        if self.request.user.is_authenticated:
            i_follow_him = self.request.user.is_following(self.object)

            context['i_follow_him'] = i_follow_him
        return context


class ShowFollowersView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = UserModel
    template_name = 'Accounts/followers_list.html'

    def test_func(self):
        profile = get_object_or_404(UserModel, pk=self.kwargs['pk'])
        return self.request.user == profile

    def get_context_data(self, *, object_list=None, **kwargs):
        user = self.request.user
        followers = user.get_followers()
        followers_list_ids = [f.user.id for f in followers]
        followers_objs = UserModel.objects.filter(id__in=followers_list_ids)
        #here afther 10 tries and 1 hour with chat gpt i find out how stupid he is and after 2 hours i mane if working!!!

        # Потребители, които аз също следвам
        following_followers = followers_objs.filter(
            id__in=followers_list_ids,  # Те ме следват
            follower_set__user=user  # Аз ги следвам обратно
        )

        # Потребители, които ме следват, но аз не ги следвам обратно
        non_following_followers = (followers_objs.filter(
            id__in=followers_list_ids  # Те ме следват
        ).exclude(
            follower_set__user=user  # Аз не ги следвам
        ))

        context = {
            'user': user,
            'following_followers': following_followers,
            'non_following_followers': non_following_followers,
        }
        return super().get_context_data(**context)