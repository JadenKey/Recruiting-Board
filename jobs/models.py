from django.conf import settings
from django.db import models
from accounts.models import Skill

class Job(models.Model):
    class Workplace(models.TextChoices):
        REMOTE = "REMOTE", "Remote"
        ONSITE = "ONSITE", "On-site"
    recruiter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="jobs")
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=200)
    salary_min = models.IntegerField(null=True, blank=True)
    salary_max = models.IntegerField(null=True, blank=True)
    workplace = models.CharField(choices=Workplace.choices, max_length=200, default=Workplace.ONSITE)
    visa_sponsorship = models.BooleanField(default=False)
    skills = models.ManyToManyField(Skill, blank=True, related_name="jobs")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} at {self.company}"
