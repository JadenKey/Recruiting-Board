from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='jobs.index'),
    path('search', views.search, name='jobs.search'),
    path('candidates', views.candidates, name='jobs.candidates'),
    path('create', views.create, name='jobs.create'),
    path('<int:id>/edit', views.edit, name='jobs.edit'),
    path('<int:id>/apply', views.apply, name='jobs.apply'),
    path('applications', views.applications, name='jobs.applications')
]
