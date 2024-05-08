from django.shortcuts import render

#  Create your views here.
from django.http import HttpResponse
from django.shortcuts import render

def login(request):
    # return HttpResponse("This is the login page.")
    return render(request, 'applicant/login.html')


def logout(request):
    # return HttpResponse("This is the logout page.")
    return render(request, 'applicant/logout.html')


def register(request):
    # return HttpResponse("This is the register page.")
    return render(request, 'applicant/register.html')


def companies(request):
    return HttpResponse("This is the list of companies.")


def company_detail(request, cid):
    # return HttpResponse(f"This is the detail view for company {cid}.")
    return render(request, 'applicant/companies.html', {cid: "dataset"})


def listings(request):
    # return HttpResponse("This is the listings page.")
    return render(request, 'applicant/listings.html')


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
    return HttpResponse(f"These are the applications for user {uid}.")
