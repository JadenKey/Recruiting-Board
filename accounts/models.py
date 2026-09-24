from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        JOB_SEEKER = "SEEKER", "Job Seeker"
        RECRUITER = "RECRUITER", "Recruiter"
    role = models.CharField(choices=Role.choices, max_length=200)
    @property
    def is_recruiter(self):
        return self.role == self.Role.RECRUITER
    @property
    def is_job_seeker(self):
        return self.role == self.Role.JOB_SEEKER
    
class RecruiterProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="recruiter_profile")
    company_name = models.CharField(max_length=200)
    def __str__(self):
        return f"{self.user.username} from {self.company_name}"
    
class Skill(models.Model):
    skill = models.CharField(max_length=200)
    def __str__(self):
        return self.skill
    
class JobSeekerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="seeker_profile")
    headline = models.CharField(max_length=200, blank=True)
    skills = models.ManyToManyField(Skill, blank=True, related_name="seekers")
    def __str__(self):
        return self.user.username
    
class Education (models.Model):
    profile = models.ForeignKey
    school = models.CharField(max_length=200)
    degree = models.CharField(max_length=200, blank=True)
    field_of_study = models.CharField(max_length=200, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    class Meta:
        ordering = ["-end_date", "-start_date"]
    def __str__(self):
        return f"{self.school} - {self.degree}"
    
class WorkExperience(models.Model):
    profile = models.ForeignKey(JobSeekerProfile, on_delete=models.CASCADE, related_name="experience")
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return f"{self.title} at {self.company}"
    
class Link(models.Model):
    profile = models.ForeignKey(JobSeekerProfile, on_delete=models.CASCADE, related_name="links")
    label = models.CharField(max_length=200) 
    url = models.URLField()
 
    def __str__(self):
        return f"{self.label}: {self.url}"


    

    
    


