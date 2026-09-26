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

class EducationInline(admin.TabularInline):
    model = Education
    extra = 0

class WorkExperienceInline(admin.StackedInline):
    model = WorkExperience
    extra = 0

class ProjectInline(admin.StackedInline):
    model = Project
    extra = 0

class LinkInline(admin.TabularInline):
    model = Link
    extra = 0

class JobSeekerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'headline', 'location']
    search_fields = ['user__username', 'headline', 'location']
    filter_horizontal = ['skills']
    inlines = [EducationInline, WorkExperienceInline, ProjectInline, LinkInline]

class RecruiterProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'company_name']
    search_fields = ['user__username', 'company_name']

admin.site.register(RecruiterProfile, RecruiterProfileAdmin)
admin.site.register(User, CustomUserAdmin)
admin.site.register(JobSeekerProfile, JobSeekerProfileAdmin)
admin.site.register(Skill)
