#  Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from company.models import JobListing, Application, Company
from utilities_static.models import Category
from applicant.models import *
from django.forms import inlineformset_factory
from django.contrib.auth.decorators import login_required
from applicant.forms.applicant_form import *
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


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
    company = Company.objects.get(id=cid)
    all_listings = JobListing.objects.filter(company_id=cid)
    return render(request, 'applicant/company_detail.html', {'company': company, 'company_listings': all_listings})


@login_required
def listings(request):
    # return HttpResponse("This is the listings page.")
    query = request.GET.get('query')
    min_pay = request.GET.get('min_pay')
    max_pay = request.GET.get('max_pay')
    due_date = request.GET.get('due_date')
    company = request.GET.get('company')
    sort = request.GET.get('sort')
    employment_type = request.GET.get('employment_type')
    category = request.GET.get('category')
    all_listings = JobListing.objects.all()
    categories = Category.objects.all()

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

    if sort == 'pay_asc':
        all_listings = all_listings.order_by('salary_low')

    elif sort == 'pay_desc':
        all_listings = all_listings.order_by('salary_high')

    elif sort == 'due_date_asc':
        all_listings = all_listings.order_by('due_date')

    elif sort == 'due_date_desc':
        all_listings = all_listings.order_by('-due_date')

    if category:
        category_id = Category.objects.get(field=category)
        all_listings = all_listings.filter(category=category_id)

    if employment_type == 'full_time':
        all_listings = all_listings.filter(employment_type_id=1)

    elif employment_type == 'part_time':
        all_listings = all_listings.filter(employment_type_id=2)

    elif employment_type == 'summer_job':
        all_listings = all_listings.filter(employment_type_id=3)

    paginator = Paginator(all_listings, 10)
    page = request.GET.get('page')

    try:
        all_listings = paginator.page(page)
    except PageNotAnInteger:
        all_listings = paginator.page(1)
    except EmptyPage:
        all_listings = paginator.page(paginator.num_pages)

    return render(request, 'applicant/listings.html', {
        'all_listings': all_listings,
        'categories': categories
    })
    #return render(request, 'applicant/listings.html', {'all_listings': all_listings, 'categories': categories})


@login_required
def listing_detail(request, lid):
    listing = JobListing.objects.get(id=lid)
    user = Applicant.objects.get(user_id=request.user.id)
    has_applied = Application.objects.filter(applicant=user, listing=listing).exists()
    return render(request, 'applicant/listing_detail.html', {'listing': listing, 'has_applied': has_applied})


@login_required
def choose_info(request, uid, lid):
    # return HttpResponse(f"This is the profile page for user {uid}.")
    return render(request, 'applicant/choose_info.html', {uid, lid})


@login_required
def profile(request):
    user = Applicant.objects.get(user_id=request.user.id)
    Experience_Form_Set = inlineformset_factory(Applicant, Experience, form=ExperienceForm, extra=1, can_delete=True)
    Education_Form_Set = inlineformset_factory(Applicant, Education, form=EducationForm, extra=1, can_delete=True)
    Resume_Form_Set = inlineformset_factory(Applicant, Resume, form=ResumeForm, extra=1, can_delete=True)
    Recommendation_Form_Set = inlineformset_factory(Applicant, Recommendation, form=RecommendationForm, extra=1,
                                                    can_delete=True)

    if request.method == 'POST':
        applicant_form = ApplicantForm(request.POST, request.FILES, instance=user)
        experience_formset = Experience_Form_Set(request.POST, instance=user)
        education_formset = Education_Form_Set(request.POST, instance=user)
        resume_formset = Resume_Form_Set(request.POST, request.FILES, instance=user)
        recommendation_formset = Recommendation_Form_Set(request.POST, instance=user)
        if (applicant_form.is_valid() and experience_formset.is_valid() and education_formset.is_valid() and
                resume_formset.is_valid() and recommendation_formset.is_valid()):
            applicant_form.save()
            experience_formset.save()
            education_formset.save()
            resume_formset.save()
            recommendation_formset.save()
            return render(request, 'applicant/listings.html')
    else:
        applicant_form = ApplicantForm(instance=user)
        experience_formset = Experience_Form_Set(instance=user)
        education_formset = Education_Form_Set(instance=user)
        resume_formset = Resume_Form_Set(instance=user)
        recommendation_formset = Recommendation_Form_Set(instance=user)

    return render(request, 'applicant/profile.html', {
        'form': applicant_form,
        'experience_formset': experience_formset,
        'education_formset': education_formset,
        'resume_formset': resume_formset,
        'recommendation_formset': recommendation_formset,
    })


@login_required
def applications(request, uid):
    # return HttpResponse(f"These are the applications for user {uid}.")
    all_applications = Application.objects.filter(applicant_id=uid)
    return render(request, 'applicant/applications.html', {'applications': all_applications})
