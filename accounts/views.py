from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .forms import (CustomUserCreationForm, JobSeekerProfileForm, EducationFormSet,
    WorkExperienceFormSet, ProjectFormSet, LinkFormSet)
from .models import JobSeekerProfile, RecruiterProfile
from reports.models import Report

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
            elif user.is_recruiter:
                RecruiterProfile.objects.create(user=user,
                    company_name=form.cleaned_data['company_name'])
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
    is_owner = request.user == profile.user
    template_data = {}
    template_data['title'] = profile.user.username
    template_data['profile'] = profile
    template_data['is_owner'] = is_owner
    template_data['has_reported'] = Report.objects.filter(reporter=request.user, reported_user=profile.user).exists()
    # the owner sees everything; recruiters only see sections marked visible
    template_data['show'] = {
        'headline': is_owner or profile.show_headline,
        'location': is_owner or profile.show_location,
        'skills': is_owner or profile.show_skills,
        'education': is_owner or profile.show_education,
        'experience': is_owner or profile.show_experience,
        'projects': is_owner or profile.show_projects,
        'links': is_owner or profile.show_links,
    }
    return render(request, 'accounts/profile_show.html', {'template_data': template_data})

def profile_edit(request):
    if not is_job_seeker(request.user):
        return redirect('home.index')
    profile, created = JobSeekerProfile.objects.get_or_create(user=request.user)
    data = request.POST if request.method == 'POST' else None
    form = JobSeekerProfileForm(data, instance=profile)
    formsets = [
        ('Education', EducationFormSet(data, instance=profile, prefix='education'), form['show_education']),
        ('Work Experience', WorkExperienceFormSet(data, instance=profile, prefix='experience'), form['show_experience']),
        ('Projects', ProjectFormSet(data, instance=profile, prefix='projects'), form['show_projects']),
        ('Links', LinkFormSet(data, instance=profile, prefix='links'), form['show_links']),
    ]
    if request.method == 'POST':
        form_valid = form.is_valid()
        formsets_valid = all([formset.is_valid() for title, formset, toggle in formsets])
        if form_valid and formsets_valid:
            form.save()
            for title, formset, toggle in formsets:
                formset.save()
            messages.success(request, 'Your profile was saved.')
            return redirect('accounts.profile_show', id=profile.id)
    template_data = {}
    template_data['title'] = 'Edit Profile'
    template_data['profile'] = profile
    template_data['form'] = form
    template_data['fields'] = [
        (form['headline'], form['show_headline']),
        (form['location'], form['show_location']),
        (form['skills'], form['show_skills']),
    ]
    template_data['formsets'] = formsets
    return render(request, 'accounts/profile_edit.html', {'template_data': template_data})