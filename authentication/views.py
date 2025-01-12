from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.conf import settings

from authentication.models import User
from authentication.forms import RegistrationForm, LoginForm
from authentication.utils import send_activation_email


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)

            if user is not None:
                auth_login(request, user)
                messages.success(request, 'You are now logged in!')
                return redirect('home')  # Replace 'home' with your desired redirect URL
            else:
                messages.error(request, 'Invalid email or password.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = LoginForm()

    return render(request, 'src/pages/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.is_active = False
            user.save()

            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            activation_link = reverse('activate', kwargs={'uidb64':uidb64,'token':token})

            activation_url = f'{settings.SITE_DOMAIN}{activation_link}'
            send_activation_email(user.email, activation_url)

            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'src/pages/signup.html', {'form': form})


def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

        if user.is_active:
            messages.warning(request, "this account has already been activated.")
            return redirect('login')

        if default_token_generator.check_token(user,token):
            user.is_active = True
            user.save()
            messages.success(request, "Your account has been activated successfully.")
            return redirect('login')
        else:
            messages.error(request, "The activation link is invalid.")
            return redirect('login')
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.error(request, "The activation link is invalid.")
        return redirect('login')
