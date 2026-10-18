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
    latitude = models.FloatField(null=True, blank=True, editable=False)
    longitude = models.FloatField(null=True, blank=True, editable=False)
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
    
class Application(models.Model):
    class Status(models.TextChoices):
        APPLIED = "APPLIED", "Applied"
        REVIEWED = "REVIEWED", "Reviewed"
        INTERVIEWING = "INTERVIEWING", "Interviewing"
        REJECTED = "REJECTED", "Rejected"
        OFFERED = "OFFERED", "Offered"
        CLOSED = "CLOSED", "Closed"
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    seeker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="applications")
    message = models.TextField(blank=True)
    status = models.CharField(choices=Status.choices, max_length=20, default=Status.APPLIED)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(fields=["job", "seeker"], name="one_application_per_job"),
        ]

    def __str__(self):
        return f"{self.seeker.username} applied to {self.job}"

class SavedSearch(models.Model):
    recruiter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="saved_searches")
    title = models.CharField(max_length=200)
    name = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=200, blank=True)
    skill = models.ForeignKey(Skill, on_delete=models.SET_NULL, null=True, blank=True)
    project = models.CharField(max_length=200, blank=True)
    # candidates the recruiter already saw
    seen = models.ManyToManyField("accounts.JobSeekerProfile", blank=True, related_name="+")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.recruiter.username})"

    # same keys as the candidates search form
    def filters(self):
        return {
            "name": self.name,
            "location": self.location,
            "skill": str(self.skill.id) if self.skill else "",
            "project": self.project,
        }
