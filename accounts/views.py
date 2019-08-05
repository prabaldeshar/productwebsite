from django.shortcuts import render, redirect
from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth, messages
from .forms import UserRegisterForm, UserProfileForm
# from .models import UserProflie
# Create your views here.
def signup(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user

            profile.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created you are now able to login!')
            return redirect('login')
    else:
        form = UserRegisterForm()
        profile_form = UserProfileForm()
    return render(request, 'accounts/register.html',{'form':form, 'profile_form': profile_form})
def login(request):
    pass

def logout(request):
    pass
