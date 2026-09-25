from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (User, RecruiterProfile, JobSeekerProfile, Skill,
    Education, WorkExperience, Project, Link)

class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'role', 'is_active', 'is_staff']
    list_filter = ['role', 'is_active', 'is_staff']
    list_editable = ['role', 'is_active']
    search_fields = ['username', 'email']
    fieldsets = UserAdmin.fieldsets + (
        ('Role', {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role', {'fields': ('role',)}),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(RecruiterProfile)
admin.site.register(JobSeekerProfile)
admin.site.register(Skill)
admin.site.register(Education)
admin.site.register(WorkExperience)
admin.site.register(Project)
admin.site.register(Link)
