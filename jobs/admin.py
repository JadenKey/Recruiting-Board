from django.contrib import admin
from .models import Job, Application

class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'recruiter', 'location', 'created_at']
    list_filter = ['workplace', 'visa_sponsorship']
    search_fields = ['title', 'company', 'description']

admin.site.register(Job, JobAdmin)
admin.site.register(Application)
