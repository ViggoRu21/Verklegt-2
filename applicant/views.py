#  Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from company.models import JobListing


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


def logout(request):
    # return HttpResponse("This is the logout page.")
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


def companies(request):
    # return HttpResponse("This is the list of companies.")
    return render(request, 'applicant/companies.html')


def company_detail(request, cid):
    # return HttpResponse(f"This is the detail view for company {cid}.")
    return render(request, 'applicant/company_detail.html', {cid: "dataset"})


def listings(request):
    # return HttpResponse("This is the listings page.")
    all_listings = JobListing.objects.all
    return render(request, 'applicant/listings.html', {'all': all_listings})


def listing_detail(request, lid):
    # return HttpResponse(f"This is the detail view for listing {lid}.")
    return render(request, 'applicant/listing_detail.html', {lid: "dataset"})


def choose_info(request, uid, lid):
    # return HttpResponse(f"This is the profile page for user {uid}.")
    return render(request, 'applicant/choose_info.html', {lid: uid})


def profile(request, uid):
    # return HttpResponse(f"This is the profile page for user {uid}.")
    return render(request, 'applicant/profile.html', {uid: "dataset"})


def profile_listings(request, uid):
    return HttpResponse(f"These are the listings for user {uid}.")


def applications(request, uid):
    #return HttpResponse(f"These are the applications for user {uid}.")
    return render(request, 'applicant/applications.html', {uid: "dataset"})
