from PartyHub_Project.Accounts.forms import UserProfileCreateForm
from PartyHub_Project.Accounts.models import UserProfile
from django.contrib.auth import login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView


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
            return redirect('profile')  # пренасочване към профила на потребителя
    else:
        form = UserProfileCreateForm()
    return render(request, 'Accounts/register.html', {'form': form})





class ProfileDetailsView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = 'accounts/profile_details.html'
    context_object_name = 'user'

    def get_object(self):
        return self.request.user


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    template_name = 'Accounts/profile_edit.html'
    success_url = reverse_lazy('profile_details')
    fields = ['profile_picture', 'bio',]

    def get_object(self):
        return self.request.user
