from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib import messages
from .forms import SignUpForm, EditProfileForm

def home(request):
    return render(request, 'authenticate/home.html', {})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ('Welcome! you are logged in now.'))
            return redirect('home')
        else:
            messages.success(request, ('Welcome! Try again.'))
            return redirect('login')
    else:
        return render(request, 'authenticate/login.html',{})

def logout_user(request):
    logout(request)
    messages.success(request, ('you have been logged out'))
    return render(request, 'authenticate/logout.html', {})

def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, ('Account create successfully'))
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'authenticate/register.html', {'form': form})

def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, ('Account Edited successfully'))
            return redirect('home')
    else:
        form = EditProfileForm(instance=request.user)
    
    return render(request, 'authenticate/edit_profile.html', {'form': form})

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, ('Password Edited successfully'))
            return redirect('home')
    else:
        form = PasswordChangeForm(user=request.user)
    
    return render(request, 'authenticate/change_password.html', {'form': form})