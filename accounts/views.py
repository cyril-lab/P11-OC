from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import CreateUserForm, AuthenticateForm
from django.contrib.auth import logout, authenticate, login
from .services.registeruser import RegisterUser


def register(request):
    """this function allows to register a user"""
    register = RegisterUser(request)
    if register.verify_post_request():
        form = CreateUserForm(request.POST)
        if register.validate_form(form):
            register.get_form_data(form)
            if register.password_verification():
                messages.warning(request,
                                 'Saisissez des mots de passe identiques')
            elif register.mail_verification():
                messages.warning(request,
                                 'Cette adresse mail est déjà utilisée')
            else:
                register.create_user()
                return redirect('login')
        return render(request, 'accounts/register.html', {'form': form})
    else:
        form = CreateUserForm()
        return render(request, 'accounts/register.html', {'form': form})


def login_user(request):
    """this function allows a user to connect"""
    if request.user.is_authenticated:
        return redirect('homepage')
    else:
        if request.method == 'POST':
            form = AuthenticateForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(request,
                                    username=username,
                                    password=password)
                if user is not None:
                    login(request, user)
                    return redirect('homepage')
                else:
                    messages.warning(request,
                                     'Adresse électronique '
                                     'ou mot de passe erroné(e)')
            return render(request, 'accounts/login.html', {'form': form})
        else:
            form = AuthenticateForm()
            return render(request, 'accounts/login.html', {'form': form})


def logout_user(request):
    """this function allows a user to disconnect"""
    logout(request)
    return redirect('homepage')


def account_user(request):
    """this function allows a user to see his account"""
    return render(request, 'accounts/account.html')
