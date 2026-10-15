from django.shortcuts import render, redirect, get_object_or_404
from jobs.models import Job, Application

def is_job_seeker(user):
    return user.is_authenticated and user.is_job_seeker

def index(request):
    if not is_job_seeker(request.user):
        return redirect('home.index')
    cart = request.session.get('cart', [])
    jobs_in_cart = Job.objects.filter(id__in=cart).prefetch_related('skills')
    template_data = {}
    template_data['title'] = 'My Job Cart'
    template_data['jobs_in_cart'] = jobs_in_cart
    template_data['applied_ids'] = list(
        Application.objects.filter(seeker=request.user).values_list('job_id', flat=True)
    )
    return render(request, 'cart/index.html', {'template_data': template_data})

def add(request, id):
    if not is_job_seeker(request.user):
        return redirect('home.index')
    get_object_or_404(Job, id=id)
    cart = request.session.get('cart', [])
    if id not in cart:
        cart.append(id)
    request.session['cart'] = cart
    return redirect('cart.index')

def remove(request, id):
    cart = request.session.get('cart', [])
    if id in cart:
        cart.remove(id)
    request.session['cart'] = cart
    return redirect('cart.index')

def clear(request):
    request.session['cart'] = []
    return redirect('cart.index')