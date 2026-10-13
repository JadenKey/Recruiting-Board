from django.conf import settings
from django.db import models
from django.db.models import Q
from jobs.models import Job

class Report(models.Model):
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="submitted_reports")
    reported_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reports_received", null=True, blank=True)
    reported_job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="reports", null=True, blank=True)
    reason = models.TextField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["reporter", "reported_user"], condition=Q(reported_user__isnull=False), name="unique_user_report"),
            models.UniqueConstraint(fields=["reporter", "reported_job"], condition=Q(reported_job__isnull=False), name="unique_job_report"),
        ]

    def __str__(self):
        if self.reported_user:
            return f"Report by {self.reporter.username} about user {self.reported_user.username}"
        elif self.reported_job:
            return f"Report by {self.reporter.username} about job {self.reported_job}"
        return f"Report by {self.reporter.username}"