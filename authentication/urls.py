from django.urls import path

from authentication.views import login, register, activate_account

urlpatterns = [
    path("login/", login, name="login"),
    path("register/", register, name="register"),
    path('activate/<str:uidb64>/<str:token>/', activate_account, name='activate')
]
