from django.urls import path
from . import views


app_name = 'home'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('details/<int:post_id>', views.DetailsView.as_view(), name='details')
]