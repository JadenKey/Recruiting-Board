from django.urls import path
from . import views
urlpatterns = [
    path('signup', views.signup, name='accounts.signup'),
    path('profile', views.profile, name='accounts.profile'),
    path('profile/<int:id>', views.profile_show, name='accounts.profile_show'),
    path('profile/edit', views.profile_edit, name='accounts.profile_edit'),
]