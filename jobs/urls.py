from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='jobs.index'),
    path('search', views.search, name='jobs.search'),
    path('map', views.job_map, name='jobs.map'),
    path('candidates', views.candidates, name='jobs.candidates'),
    path('create', views.create, name='jobs.create'),
    path('<int:id>/edit', views.edit, name='jobs.edit'),
    path('<int:id>/apply', views.apply, name='jobs.apply'),
    path('applications/<int:id>/status', views.application_status, name='jobs.application_status'),
    path('<int:id>/pipeline', views.pipeline, name='jobs.pipeline'),
    path('applications', views.applications, name='jobs.applications'),
    path('applications/<int:id>/candidate/', views.candidate_details, name='jobs.candidate_details'),
    path("<int:id>/recommendations/", views.candidate_recommendations, name="jobs.candidate_recommendations"),
    path('export/<str:kind>', views.export_csv, name='jobs.export_csv'),
]
