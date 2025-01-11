from django.shortcuts import render

# Create your views here.
def login(request):
    return render(request, 'src/pages/login.html')

def register(request):
    return render(request, 'src/pages/signup.html')