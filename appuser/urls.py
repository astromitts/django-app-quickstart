from django.urls import path
from appuser import views

urlpatterns = [
    path('register/', views.Register.as_view(), name='register'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('api/register/', views.RegisterAPI.as_view(), name='register_api'),
    path('eula/', views.EULA.as_view(), name='eula'),
    path('privacy-policy/', views.PrivacyPolicy.as_view(), name='privacy_policy'),
    path('policy-agreement/', views.PolicyAgreement.as_view(), name='policy_agreement'),
]
