from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .forms import (CustomUserCreationForm, JobSeekerProfileForm, EducationFormSet,
    WorkExperienceFormSet, ProjectFormSet, LinkFormSet)
from .models import JobSeekerProfile

def is_job_seeker(user):
    return user.is_authenticated and user.is_job_seeker

def signup(request):
    template_data = {}
    template_data['title'] = 'Sign Up'
    if request.method == 'GET':
        template_data['form'] = CustomUserCreationForm()
        return render(request, 'accounts/signup.html',
            {'template_data': template_data})
    elif request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user.is_job_seeker:
                JobSeekerProfile.objects.create(user=user)
            return redirect('home.index')
        else:
            template_data['form'] = form
            return render(request, 'accounts/signup.html',
                {'template_data': template_data})

def profile(request):
    if not is_job_seeker(request.user):
        return redirect('home.index')
    profile, created = JobSeekerProfile.objects.get_or_create(user=request.user)
    return redirect('accounts.profile_show', id=profile.id)

def profile_show(request, id):
    profile = get_object_or_404(JobSeekerProfile, id=id)
    if not request.user.is_authenticated:
        return redirect('home.index')
    if request.user != profile.user and not request.user.is_recruiter:
        return redirect('home.index')
    if request.user != profile.user and not profile.is_public:
        return redirect('home.index')
    template_data = {}
    template_data['title'] = profile.user.username
    template_data['profile'] = profile
    template_data['is_owner'] = request.user == profile.user
    return render(request, 'accounts/profile_show.html', {'template_data': template_data})

def profile_edit(request):
    if not is_job_seeker(request.user):
        return redirect('home.index')
    profile, created = JobSeekerProfile.objects.get_or_create(user=request.user)
    template_data = {}
    template_data['title'] = 'Edit Profile'
    template_data['profile'] = profile
    if request.method == 'GET':
        template_data['form'] = JobSeekerProfileForm(instance=profile)
        template_data['formsets'] = [
            ('Education', EducationFormSet(instance=profile, prefix='education')),
            ('Work Experience', WorkExperienceFormSet(instance=profile, prefix='experience')),
            ('Projects', ProjectFormSet(instance=profile, prefix='projects')),
            ('Links', LinkFormSet(instance=profile, prefix='links')),
        ]
        return render(request, 'accounts/profile_edit.html', {'template_data': template_data})
    elif request.method == 'POST':
        form = JobSeekerProfileForm(request.POST, instance=profile)
        formsets = [
            ('Education', EducationFormSet(request.POST, instance=profile, prefix='education')),
            ('Work Experience', WorkExperienceFormSet(request.POST, instance=profile, prefix='experience')),
            ('Projects', ProjectFormSet(request.POST, instance=profile, prefix='projects')),
            ('Links', LinkFormSet(request.POST, instance=profile, prefix='links')),
        ]
        if form.is_valid() and all(formset.is_valid() for title, formset in formsets):
            form.save()
            for title, formset in formsets:
                formset.save()
            messages.success(request, 'Your profile was saved.')
            return redirect('accounts.profile_show', id=profile.id)
        else:
            template_data['form'] = form
            template_data['formsets'] = formsets
            return render(request, 'accounts/profile_edit.html', {'template_data': template_data})