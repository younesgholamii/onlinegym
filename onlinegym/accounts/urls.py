from django.urls import path
from . import views


app_name = 'accounts'
urlpatterns = [
    path('userregister/', views.UserRegisterView.as_view(), name='user_register'),
    path('login/', views.UserLoginView.as_view(), name='user_login'),
    path('logout/', views.UserLogoutView.as_view(), name='user_logout'),
    path('profile/<int:user_id>/', views.UserProfileView.as_view(), name='user_profile'),
    path('profile/edit/', views.UserProfileEditView.as_view(), name='user_profile_edit'),
]