
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from company.models import *


def login_page(request):
    return render(request, 'company/login.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('company:listings')
        else:
            messages.error(request, 'Invalid username or password')
            return render(request, 'company/login.html')

    else:
        return render(request, 'company/login.html')


def logout_view(request):
    logout(request)
    return render(request, 'company/logout.html')


def register_page(request):
    return render(request, 'company/register.html')


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        company_ssn = request.POST.get('company_ssn')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password == confirm_password:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            recruiter = Recruiter(user=user, company_ssn=company_ssn)
            recruiter.save()
            return render(request, 'company/login.html')
        else:
            messages.error(request, 'Passwords do not match')
            return render(request, 'company/register.html')


def forgot(request):
    return render(request, 'company/forgot.html')


@login_required
def company_detail(request, cid):
    company = Company.objects.get(id=cid)
    return render(request, 'company/company_detail.html', {'company': company})


@login_required
def listings(request):
    recruiter_info = Recruiter.objects.get(user_id=request.user.id)
    company = Company.objects.get(company_ssn=recruiter_info.company_ssn)
    query = request.GET.get('query')
    if query:
        all_listings = JobListing.objects.filter(job_title__icontains=query, id=company.id)
    else:
        all_listings = JobListing.objects.filter(id=company.id)
    return render(request, 'company/listings.html', {'listings': all_listings})


@login_required
def listing_detail(request, lid):
    # return HttpResponse(f"This is the detail view for listing {lid}.")
    listing = JobListing.objects.filter(id=lid)
    return render(request, 'company/listing_detail.html', {'listing': listing})


@login_required
def profile(request, uid):
    # return HttpResponse(f"This is the profile page for user {uid}.")
    user = Recruiter.objects.filter(id=uid)
    return render(request, 'company/profile.html', {'user': user})


@login_required
def profile_listings(request, uid):
    listing = JobListing.objects.filter(recruiter__id=uid)
    return render(request, 'company/profile_listings.html', {'listing': listing})


@login_required
def profile_listing_detail(request, uid, lid):
    # Get the specific listing directly for the user with id `uid`
    listing = JobListing.objects.filter(recruiter__id=uid, id=lid).first()
    return render(request, 'company/profile_listing_detail.html', {'listing': listing})


@login_required
def listing_applicants(request, uid, lid):
    applicants = Application.objects.filter(listing__id=lid)
    return render(request, 'company/listing_applicants.html', {'applications': applicants})


@login_required
def applicant_detail(request, uid, lid, aid):
    application = Application.objects.filter(applicant__id=aid, listing__id=lid).first()
    return render(request, 'company/applicant_detail.html', {'applicant': application})