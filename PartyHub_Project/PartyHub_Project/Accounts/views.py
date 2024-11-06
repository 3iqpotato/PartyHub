from PartyHub_Project.Accounts.forms import UserProfileCreateForm
from django.contrib.auth import login
from django.shortcuts import render, redirect


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
            return redirect('index')  # пренасочване към профила на потребителя
    else:
        form = UserProfileCreateForm()
    return render(request, 'Accounts/register.html', {'form': form})