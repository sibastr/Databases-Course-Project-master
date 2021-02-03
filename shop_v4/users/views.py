from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import users
from users.admin import UserCreationForm, UserChangeForm, ProfileUpdateForm


# TODO class-based register and profile views
def register(request):

    if request.method == 'POST':

        form = UserCreationForm(request.POST)

        if form.is_valid():
            
            form.save()
            email = form.cleaned_data.get('email')
            messages.success(request, f'Создан аккаунт для {email}!')
            return redirect('login')
    else:
        form = users.admin.UserCreationForm()

    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserChangeForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Ваш аккаун был обновлен!')
            return redirect('profile')
    else:
        u_form = UserChangeForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)
