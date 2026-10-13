from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from accounts.models import User
from reports.models import Report
from jobs.models import Job
from .forms import ReportForm

@login_required
def report_user(request, id):
    reported_user = get_object_or_404(User, id=id)

    if reported_user == request.user:
        messages.warning(request, 'You cannot report yourself.')
        return redirect('home.index')
    if ((request.user.is_recruiter and reported_user.is_recruiter)
        or (request.user.is_job_seeker and reported_user.is_job_seeker)
        or not (request.user.is_recruiter or request.user.is_job_seeker)):
        messages.warning(request, 'You do not have permission to report this user.')
        return redirect('home.index')

    if Report.objects.filter(reporter=request.user, reported_user=reported_user).exists():
        messages.info(request, 'You have already reported this user.')
        return redirect('home.index')

    template_data = {}
    template_data['title'] = 'Report User'
    template_data['subtitle'] = f"You are reporting {reported_user.username}"

    if request.method == 'GET':
        template_data['form'] = ReportForm()
        return render(request, 'reports/report.html', {'template_data': template_data})
    elif request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.reporter = request.user
            report.reported_user = reported_user
            report.save()
            return redirect('home.index')
        else:
            template_data['form'] = form
            return render(request, 'reports/report.html', {'template_data': template_data})


@login_required
def report_job(request, id):
    reported_job = get_object_or_404(Job, id=id)

    if reported_job.recruiter == request.user:
        messages.warning(request, 'You cannot report your own job.')
        return redirect('home.index')
    if request.user.is_recruiter:
        messages.warning(request, 'You do not have permission to report this job.')
        return redirect('home.index')

    if Report.objects.filter(reporter=request.user, reported_job=reported_job).exists():
        messages.info(request, 'You have already reported this job.')
        return redirect('home.index')

    template_data = {}
    template_data['title'] = 'Report Job'
    template_data['subtitle'] = f"You are reporting {reported_job.title}"

    if request.method == 'GET':
        template_data['form'] = ReportForm()
        return render(request, 'reports/report.html', {'template_data': template_data})
    elif request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.reporter = request.user
            report.reported_job = reported_job
            report.save()
            return redirect('home.index')
        else:
            template_data['form'] = form
            return render(request, 'reports/report.html', {'template_data': template_data})