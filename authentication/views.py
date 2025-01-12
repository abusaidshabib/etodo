from django.shortcuts import render, redirect

from authentication.forms import RegistrationForm


def login(request):
    return render(request, 'src/pages/login.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'src/pages/signup.html', {'form': form})