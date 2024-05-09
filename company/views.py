
#  Create your views here.
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


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
@login_required
def company_detail(request, cid):
    # return HttpResponse(f"This is the detail view for company {cid}.")
    return render(request, 'company/company_detail.html', {cid})


@login_required
def listings(request):
    # return HttpResponse("This is the listings page.")
    return render(request, 'company/listings.html')


@login_required
def listing_detail(request, lid):
    # return HttpResponse(f"This is the detail view for listing {lid}.")
    return render(request, 'company/listing_detail.html', {lid: "dataset"})


@login_required
def profile(request, uid):
    # return HttpResponse(f"This is the profile page for user {uid}.")
    return render(request, 'company/profile.html', {uid: "dataset"})


@login_required
def profile_listings(request, uid):
    # return HttpResponse(f"These are the listings for user {uid}.")
    return render(request, 'company/profile_listings.html', {uid: "dataset"})


@login_required
def profile_listing_detail(request, uid, lid):
    # return HttpResponse(f"This is the detail view for listing {lid} of user {uid}.")
    return render(request, 'company/profile_listing_detail.html', {uid: "dataset", lid: "Dataset"})


@login_required
def listing_applicants(request, uid, lid):
    # return HttpResponse(f"These are the applicants for listing {lid} of user {uid}.")
    return render(request, 'company/listing_applicants.html', {uid: "dataset", lid: "Dataset"})


@login_required
def applicant_detail(request, uid, lid, aid):
    # return HttpResponse(f"This is the detail view for applicant {aid} for listing {lid} of user {uid}.")
    return render(request, 'company/applicant_detail.html', {uid: "dataset", lid: "Dataset", aid: "Dataset"})
