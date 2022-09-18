from django.urls import path
from accounts import views


urlpatterns = [
    path("login/",views.loginUser,name='login'),
    path("signup/",views.signin,name="signin"),
    path("verify",views.logoutUser,name='logout'),
    path("logout",views.logoutUser,name='logout'),
    path("forgot-password",views.forgot),
    path("reset-password",views.reset),
    path("change-email",views.change_email),
]