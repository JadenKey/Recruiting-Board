from django.urls import path
from . import views
urlpatterns = [
    path('', views.inbox, name='messaging.inbox'),
    path('<int:id>', views.thread, name='messaging.thread'),
    path('<int:id>/email', views.email_candidate, name='messaging.email'),
]
