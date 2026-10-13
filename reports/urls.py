from django.urls import path
from . import views

urlpatterns = [
    path("user/<int:id>/", views.report_user, name="reports.user"),
    path("job/<int:id>/", views.report_job, name="reports.job"),
]