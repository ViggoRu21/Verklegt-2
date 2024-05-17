
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from company.models import Recruiter, Company, JobListing, Application
from django.core.exceptions import ObjectDoesNotExist


def login_page(request):
    return render(request, 'company/login.html')


def login_view(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            try:
                recruiter = user.recruiter
                return redirect('company:listings')
            except ObjectDoesNotExist:
                messages.error(request, 'You are not an recruiter')
                return redirect('applicant:login_view'
                                )
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
        company_ssn = request.POST.get('CSSID')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
            return render(request, 'company/register.html')

        if password == confirm_password and len(password) >= 8:
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
def company_detail(request):
    # return HttpResponse(f"This is the detail view for company {cid}.")
    company = Company.objects.get(ssn=request.user.recruiter.company_ssn)
    return render(request, 'company/company_detail.html', {'company': company})


@login_required
def listings(request):
    recruiter_info = Recruiter.objects.get(user_id=request.user.id)
    company = Company.objects.get(ssn=recruiter_info.company_ssn)
    query = request.GET.get('query')
    if query:
        all_listings = JobListing.objects.filter(job_title__icontains=query, company_id=company.id)
    else:
        all_listings = JobListing.objects.filter(company_id=company.id)
    return render(request, 'company/listings.html', {'listings': all_listings})


@login_required
def listing_detail(request, lid):
    # return HttpResponse(f"This is the detail view for listing {lid}.")
    listing = JobListing.objects.get(id=lid)
    return render(request, 'company/listing_detail.html', {'listing': listing})


@login_required
def profile(request):
    # return HttpResponse(f"This is the profile page for user {uid}.")
    user = Recruiter.objects.filter(user_id=request.user.id)

    return render(request, 'company/profile.html', {'user': user})


@login_required
def profile_listings(request):
    user_listings = JobListing.objects.filter(recruiter_id=request.user.id)
    return render(request, 'company/profile_listings.html', {'listings': user_listings})


@login_required
def profile_listing_detail(request, lid):
    listing = JobListing.objects.get(id=lid)
    return render(request, 'company/profile_listing_detail.html', {'listing': listing})


@login_required
def listing_applicants(request, lid):
    applicants = Application.objects.filter(listing_id=lid)
    return render(request, 'company/listing_applicants.html', {'applications': applicants})


@login_required
def applicant_detail(request, lid, aid):
    application = Application.objects.get(applicant_id=aid, listing_id=lid)
    return render(request, 'company/applicant_detail.html', {'applicant': application})
