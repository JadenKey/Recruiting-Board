from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import User
from .models import Message
from .forms import MessageForm, EmailForm

def is_recruiter(user):
    return user.is_authenticated and user.is_recruiter

def inbox(request):
    if not request.user.is_authenticated:
        return redirect('home.index')
    my_messages = Message.objects.filter(
        Q(sender=request.user) | Q(recipient=request.user))
    people = []
    for message in my_messages:
        if message.sender == request.user:
            other = message.recipient
        else:
            other = message.sender
        if other not in people:
            people.append(other)
    template_data = {}
    template_data['title'] = 'Messages'
    template_data['people'] = people
    return render(request, 'messaging/inbox.html', {'template_data': template_data})

def thread(request, id):
    if not request.user.is_authenticated:
        return redirect('home.index')
    other = get_object_or_404(User, id=id)
    if other == request.user:
        return redirect('messaging.inbox')
    template_data = {}
    template_data['title'] = other.username
    template_data['other'] = other
    template_data['conversation'] = Message.objects.filter(
        Q(sender=request.user, recipient=other) | Q(sender=other, recipient=request.user))
    if request.method == 'GET':
        template_data['form'] = MessageForm()
        return render(request, 'messaging/thread.html', {'template_data': template_data})
    elif request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.recipient = other
            message.save()
            return redirect('messaging.thread', id=other.id)
        else:
            template_data['form'] = form
            return render(request, 'messaging/thread.html', {'template_data': template_data})

def email_candidate(request, id):
    if not is_recruiter(request.user):
        return redirect('home.index')
    candidate = get_object_or_404(User, id=id, role=User.Role.JOB_SEEKER)
    template_data = {}
    template_data['title'] = 'Email a Candidate'
    template_data['candidate'] = candidate
    if request.method == 'GET':
        template_data['form'] = EmailForm()
        return render(request, 'messaging/email.html', {'template_data': template_data})
    elif request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            if not candidate.email:
                messages.error(request,
                    f'{candidate.username} does not have an email address saved.')
            else:
                try: 
                    send_mail(
                        form.cleaned_data['subject'],
                        form.cleaned_data['body'],
                        None,
                        [candidate.email],
                    )
                except OSError:
                    messages.error(request, 'Email could not be sent. Please try again later.')
                    template_data['form'] = form
                    return render(request, 'messaging/email.html', {'template_data': template_data})
                messages.success(request, f'Email sent to {candidate.username}.')
            return redirect('jobs.candidates')
        else:
            template_data['form'] = form
            return render(request, 'messaging/email.html', {'template_data': template_data})