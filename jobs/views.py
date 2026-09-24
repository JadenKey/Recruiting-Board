from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import Skill
from .models import Job
from .forms import JobForm

def is_recruiter(user):
    return user.is_authenticated and user.is_recruiter

def index(request):
    if not is_recruiter(request.user):
        return redirect('home.index')
    template_data = {}
    template_data['title'] = 'My Job Posts'
    template_data['jobs'] = Job.objects.filter(recruiter=request.user)
    return render(request, 'jobs/index.html', {'template_data': template_data})

def create(request):
    if not is_recruiter(request.user):
        return redirect('home.index')
    template_data = {}
    template_data['title'] = 'Post a Job'
    if request.method == 'GET':
        template_data['form'] = JobForm()
        return render(request, 'jobs/form.html', {'template_data': template_data})
    elif request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.recruiter = request.user
            job.save()
            form.save_m2m()
            return redirect('jobs.index')
        else:
            template_data['form'] = form
            return render(request, 'jobs/form.html', {'template_data': template_data})

def edit(request, id):
    if not is_recruiter(request.user):
        return redirect('home.index')
    job = get_object_or_404(Job, id=id, recruiter=request.user)
    template_data = {}
    template_data['title'] = 'Edit Job'
    if request.method == 'GET':
        template_data['form'] = JobForm(instance=job)
        return render(request, 'jobs/form.html', {'template_data': template_data})
    elif request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('jobs.index')
        else:
            template_data['form'] = form
            return render(request, 'jobs/form.html', {'template_data': template_data})

def search(request):
    jobs = Job.objects.all()
    title = request.GET.get('title')
    if title:
        jobs = jobs.filter(title__icontains=title)
    location = request.GET.get('location')
    if location:
        jobs = jobs.filter(location__icontains=location)
    skill = request.GET.get('skill')
    if skill:
        jobs = jobs.filter(skills__id=skill)
    salary_min = request.GET.get('salary_min')
    if salary_min:
        jobs = jobs.filter(salary_max__gte=salary_min)
    salary_max = request.GET.get('salary_max')
    if salary_max:
        jobs = jobs.filter(salary_min__lte=salary_max)
    workplace = request.GET.get('workplace')
    if workplace:
        jobs = jobs.filter(workplace=workplace)
    if request.GET.get('visa_sponsorship'):
        jobs = jobs.filter(visa_sponsorship=True)
    template_data = {}
    template_data['title'] = 'Search Jobs'
    template_data['jobs'] = jobs.distinct()
    template_data['skills'] = Skill.objects.all()
    template_data['filters'] = request.GET
    return render(request, 'jobs/search.html', {'template_data': template_data})
