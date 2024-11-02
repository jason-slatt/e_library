from django.urls import path
from . import views

urlpatterns = [     
    path('registration/', views.RegistrationView.as_view(), name = 'registration'),
    path('login/', views.LoginView.as_view(), name = 'login'),
    path('passwordReset/', views.PasswordResetView.as_view(), name = 'password-reset'),
    path('password-reset-confirm/<str:uid64>/<str:token>/', views.PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('Activate-account/<str:uid64>/<str:token>/', views.ActivateAccountView.as_view(), name = 'actiavate')

]