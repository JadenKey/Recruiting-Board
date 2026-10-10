from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.db.models import Q
from accounts.models import Skill, JobSeekerProfile, User
from .models import Job, Application
from .forms import JobForm, ApplicationForm

def is_recruiter(user):
    return user.is_authenticated and user.is_recruiter
def is_job_seeker(user):
    return user.is_authenticated and user.is_job_seeker

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
    if is_job_seeker(request.user):
        template_data['applied_ids'] = set(
            Application.objects.filter(seeker=request.user).values_list('job_id', flat=True)
        )
    return render(request, 'jobs/search.html', {'template_data': template_data})

def candidates(request):
    if not is_recruiter(request.user):
        return redirect('home.index')

    candidates = JobSeekerProfile.objects.filter(
        user__role=User.Role.JOB_SEEKER,
    ).select_related('user').prefetch_related('skills', 'projects')

    name = request.GET.get('name', '').strip()
    if name:
        candidates = candidates.filter(user__username__icontains=name)

    location = request.GET.get('location')
    if location:
        candidates = candidates.filter(show_location=True, location__icontains=location)

    skill = request.GET.get('skill')
    if skill:
        candidates = candidates.filter(show_skills=True, skills__id=skill)

    project = request.GET.get('project')
    if project:
        candidates = candidates.filter(show_projects=True).filter(
            Q(projects__title__icontains=project) |
            Q(projects__description__icontains=project)
        )

    template_data = {}
    template_data['title'] = 'Search Candidates'
    template_data['candidates'] = candidates.distinct().order_by('user__username')
    template_data['skills'] = Skill.objects.all()
    template_data['filters'] = request.GET

    return render(
        request,
        'jobs/candidates.html',
        {'template_data': template_data}
    )

def apply(request, id):
    if request.method != 'POST':
        return redirect('jobs.search')
    if not request.user.is_authenticated:
        return redirect(f"{reverse('login')}?next={reverse('jobs.search')}")
    if not is_job_seeker(request.user):
        messages.error(request, 'Only Job Seekers can apply to jobs.')
        return redirect('jobs.search')

    job = get_object_or_404(Job, id=id)
    form = ApplicationForm(request.POST)
    if form.is_valid():
        application, created = Application.objects.get_or_create(
            job=job,
            seeker=request.user,
            defaults={'message': form.cleaned_data['message']},
        )
        if created:
            messages.success(request, f'You applied to {job.title} at {job.company}.')
        else:
            messages.info(request, f'You already applied to {job.title}.')

    next_url = request.POST.get('next')
    if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        return redirect(next_url)
    return redirect('jobs.search')

def applications(request):
    if not is_job_seeker(request.user):
        return redirect('home.index')

    applications = Application.objects.filter(seeker=request.user).select_related('job')
    template_data = {}
    template_data['title'] = 'Applications'
    template_data['applications'] = applications

    return render(request, 'jobs/applications.html', {'template_data': template_data})

# the board shows the stages left to right, with rejected on the end
BOARD = [
    Application.Status.APPLIED,
    Application.Status.REVIEWED,
    Application.Status.INTERVIEWING,
    Application.Status.OFFERED,
    Application.Status.CLOSED,
    Application.Status.REJECTED,
]

def pipeline(request, id):
    if not is_recruiter(request.user):
        return redirect('home.index')
    job = get_object_or_404(Job, id=id, recruiter=request.user)
    columns = []
    for status in BOARD:
        columns.append({
            'value': status,
            'label': status.label,
            'applications': job.applications.filter(status=status),
        })
    template_data = {}
    template_data['title'] = 'Pipeline'
    template_data['job'] = job
    template_data['columns'] = columns
    return render(request, 'jobs/pipeline.html', {'template_data': template_data})

def application_status(request, id):
    if not is_recruiter(request.user):
        return redirect('home.index')
    application = get_object_or_404(Application, id=id, job__recruiter=request.user)
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in dict(Application.Status.choices):
            application.status = status
            application.save()
            messages.success(request, f'Moved {application.seeker.username} to {application.get_status_display()}.')
    return redirect('jobs.pipeline', id=application.job.id)

def candidate_details(request, id):
    if not is_recruiter(request.user):
        return redirect('home.index')
    application = get_object_or_404(Application.objects.select_related('seeker', 'job'), id=id, job__recruiter=request.user)
    candidate = get_object_or_404(JobSeekerProfile.objects.select_related('user').prefetch_related('skills', 'education', 'experience', 'projects', 'links',), user=application.seeker)

    template_data = {}
    template_data['title'] = 'Candidate Details'
    template_data['application'] = application
    template_data['candidate'] = candidate

    return render(request, 'jobs/candidate_details.html', {'template_data': template_data})
