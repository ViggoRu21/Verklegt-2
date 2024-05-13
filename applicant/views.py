#  Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from company.models import JobListing, Application, Company
from applicant.models import *
from django.contrib.auth.decorators import login_required


def login_page(request):
    # return HttpResponse("This is the login page.")
    return render(request, 'applicant/login.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('applicant:listings')
        else:
            messages.error(request, 'Invalid username or password')
            return render(request, 'applicant/login.html')

    else:
        return render(request, 'applicant/login.html')


def logout_user(request):
    # return HttpResponse("This is the logout page.")
    logout(request)
    return render(request, 'applicant/logout.html')


def register_page(request):
    # return HttpResponse("This is the register page.")
    return render(request, 'applicant/register.html')


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password == confirm_password:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            applicant = Applicant(user=user)
            applicant.save()
            return render(request, 'applicant/login.html')
        else:
            messages.error(request, 'Passwords do not match')
            return render(request, 'applicant/register.html')


@login_required
def companies(request):
    # return HttpResponse("This is the list of companies.")
    all_companies = Company.objects.all()
    return render(request, 'applicant/companies.html', {"all_companies": all_companies})


@login_required
def company_detail(request, cid):
    # return HttpResponse(f"This is the detail view for company {cid}.")
    # return render(request, 'applicant/company_detail.html', {cid: "dataset"})
    company = Company.objects.filter(id=cid)
    return render(request, 'applicant/company_detail.html', {'company': company})


@login_required
def listings(request):
    # return HttpResponse("This is the listings page.")
    query = request.GET.get('query')
    min_pay = request.GET.get('min_pay')
    max_pay = request.GET.get('max_pay')
    due_date = request.GET.get('due_date')
    company = request.GET.get('company')
    all_listings = JobListing.objects.all()

    if query:
        all_listings = all_listings.filter(job_title__icontains=query)

    if min_pay:
        all_listings = all_listings.filter(salary_low__gte=min_pay)

    if due_date:
        due_date = timezone.datetime.strptime(due_date, "%Y-%m-%d").date()
        all_listings = all_listings.filter(due_date__gte=due_date)

    if max_pay:
        all_listings = all_listings.filter(salary_high__lte=max_pay)

    if company:
        all_listings = all_listings.filter(company__company_name__icontains=company)

    return render(request, 'applicant/listings.html', {'all_listings': all_listings})


@login_required
def listing_detail(request, lid):
    # return HttpResponse(f"This is the detail view for listing {lid}.")
    listing = JobListing.objects.filter(id=lid)
    return render(request, 'applicant/listing_detail.html', {'wanted_listing': listing})


@login_required
def choose_info(request, uid, lid):
    # return HttpResponse(f"This is the profile page for user {uid}.")
    return render(request, 'applicant/choose_info.html', {uid, lid})


@login_required
def profile(request, uid):
    # return HttpResponse(f"This is the profile page for user {uid}.")
    user = Applicant.objects.filter(user_id=uid)
    return render(request, 'applicant/profile.html', {'user': user})


@login_required
def applications(request, uid):
    # return HttpResponse(f"These are the applications for user {uid}.")
    all_applications = Application.objects.filter(applicant_id=uid)
    return render(request, 'applicant/applications.html', {'application': all_applications})
