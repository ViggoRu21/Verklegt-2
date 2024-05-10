#  Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from company.models import JobListing, Company
from company.models import JobListing, Company
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
    try:
        company = Company.objects.get(id=cid)
    except Company.DoesNotExist:
        from django.http import Http404
        raise Http404("Company does not exist")
    return render(request, 'applicant/company_detail.html', {'company': company})


@login_required(login_url="applicant/login")
def listings(request):
    # return HttpResponse("This is the listings page.")
    all_listings = JobListing.objects.all()
    return render(request, 'applicant/listings.html', {'all_listings': all_listings})


@login_required
def listing_detail(request, lid):
    # return HttpResponse(f"This is the detail view for listing {lid}.")
    return render(request, 'applicant/listing_detail.html', {lid: "dataset"})


@login_required
def choose_info(request, uid, lid):
    # return HttpResponse(f"This is the profile page for user {uid}.")
    return render(request, 'applicant/choose_info.html', {lid: uid})


@login_required
def profile(request, uid):
    # return HttpResponse(f"This is the profile page for user {uid}.")
    return render(request, 'applicant/profile.html', {uid: "dataset"})


@login_required
def profile_listings(request, uid):
    #return HttpResponse(f"These are the listings for user {uid}.")
    return render(request, 'applicant/applications.html', {uid: "dataset"})


@login_required
def applications(request, uid):
    # return HttpResponse(f"These are the applications for user {uid}.")
    return render(request, 'applicant/applications.html', {uid: "dataset"})
