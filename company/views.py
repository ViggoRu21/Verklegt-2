
#  Create your views here.
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from company.models import *


def login_page(request):
    # return HttpResponse("This is the login page.")
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


def logout(request):
    # return HttpResponse("This is the logout page.")
    return render(request, 'company/logout.html')


def register_page(request):
    # return HttpResponse("This is the register page.")
    return render(request, 'company/register.html')


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password == confirm_password:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            return render(request, 'company/login.html')
        else:
            messages.error(request, 'Passwords do not match')
            return render(request, 'company/register.html')


def forgot(request):
    # return HttpResponse("You forgot your password")
    return render(request, 'company/forgot.html')


@login_required
def company_detail(request, cid):
    # return HttpResponse(f"This is the detail view for company {cid}.")
    for company in Company.objects.all():
        if company.id == cid:
            return render(request, 'company/company_detail.html', {'company': company})


@login_required
def listings(request, cid):
    # return HttpResponse("This is the listings page.")
    all_listings = []
    for listing in JobListing.objects.all():
        if listing.company.id == cid:
            all_listings.append(listing)
    return render(request, 'company/listings.html', {'listings': all_listings})


@login_required
def listing_detail(request, lid):
    # return HttpResponse(f"This is the detail view for listing {lid}.")
    for listing in JobListing.objects.all():
        if listing.id == lid:
            return render(request, 'company/listing_detail.html', {'listing': listing})


@login_required
def profile(request, uid):
    # return HttpResponse(f"This is the profile page for user {uid}.")
    for user in Recruiter.objects.all():
        if user.id == uid:
            return render(request, 'company/profile.html', {'user': user})


@login_required
def profile_listings(request, uid):
    # return HttpResponse(f"These are the listings for user {uid}.")
    all_listings = JobListing.objects.all()
    wanted_listings = []
    for listing in all_listings:
        if listing.recruiter.id == uid:
            wanted_listings.append(listing)
    return render(request, 'company/profile_listings.html', {'listings': wanted_listings})


@login_required
def profile_listing_detail(request, uid, lid):
    # return HttpResponse(f"This is the detail view for listing {lid} of user {uid}.")
    all_listings = JobListing.objects.all()
    for listing in all_listings:
        if listing.recruiter.id == uid:
            if listing.id == lid:
                return render(request, 'company/profile_listing_detail.html', {'listing': listing})


@login_required
def listing_applicants(request, uid, lid):
    # return HttpResponse(f"These are the applicants for listing {lid} of user {uid}.")
    all_listings = JobListing.objects.all()
    wanted_listing = None
    for listing in all_listings:
        if listing.recruiter.id == uid:
            if listing.id == lid:
                wanted_listing = listing
                break
    applicants = []
    all_applications = Application.objects.all()
    for application in all_applications:
        if application.listing.id == lid:
            applicants.append(application)

    return render(request, 'company/listing_applicants.html', {'applications': applicants})


@login_required
def applicant_detail(request, uid, lid, aid):
    # return HttpResponse(f"This is the detail view for applicant {aid} for listing {lid} of user {uid}.")
    all_applications = Application.objects.all()
    for application in all_applications:
        if application.applicant.id == aid:
            if application.listing.id == lid:
                return render(request, 'company/applicant_detail.html', {'applicant': application})
