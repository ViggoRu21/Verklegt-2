from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpRequest, HttpResponse
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from company.models import (Company, Recruiter, JobListing, Applicant, Application, ApplicationEducation,
                            ApplicationResume, ApplicationRecommendations, ApplicationWorkExperience)
from utilities_static.models import Category
from django.forms import inlineformset_factory
from applicant.models import User
from django.contrib.auth.decorators import login_required
from applicant.forms.applicant_form import *
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q


def login_page(request: HttpRequest) -> HttpResponse:
    return render(request, 'applicant/login.html')


def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        username: str = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username.lower(), password=password)
        if user is not None:
            login(request, user)
            try:
                applicant = user.applicant
                return redirect('applicant:listings')
            except ObjectDoesNotExist:
                messages.error(request, 'You are not an applicant')
                return redirect('company:login_view')
        else:
            messages.error(request, 'Invalid username or password')
            return render(request, 'applicant/login.html')

    else:
        return render(request, 'applicant/login.html')


def logout_user(request: HttpRequest) -> HttpResponse:
    logout(request)
    return render(request, 'applicant/logout.html')


def register_page(request: HttpRequest) -> HttpResponse:
    return render(request, 'applicant/register.html')


def register_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        username: str = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
            return render(request, 'applicant/register.html')

        if password == confirm_password:
            user = User.objects.create_user(username=username.lower(), email=email, password=password)
            user.save()
            applicant = Applicant(user=user)
            applicant.save()
            return render(request, 'applicant/login.html')
        else:
            messages.error(request, 'Passwords do not match')
            return render(request, 'applicant/register.html')


@login_required
def companies(request: HttpRequest) -> HttpResponse:
    company = request.GET.get('company_name')
    all_companies = Company.objects.all()
    if company:
        all_companies = all_companies.filter(name__icontains=company)
    return render(request, 'applicant/companies.html', {"all_companies": all_companies})

@login_required
def company_detail(request: HttpRequest, cid) -> HttpResponse:
    company = Company.objects.get(id=cid)
    all_listings = JobListing.objects.filter(company_id=cid)
    return render(request, 'applicant/company_detail.html', {'company': company, 'company_listings': all_listings})


@login_required
def listings(request: HttpRequest) -> HttpResponse:
    query = request.GET.get('query')
    min_pay = request.GET.get('min_pay')
    max_pay = request.GET.get('max_pay')
    due_date = request.GET.get('due_date')
    company = request.GET.get('company')
    sort = request.GET.get('sort')
    employment_type = request.GET.get('employment_type')
    applied_status = request.GET.get('applied_status')
    category = request.GET.get('category')
    all_listings = JobListing.objects.all()
    categories = Category.objects.all()

    if applied_status == 'show_applied':
        user = Applicant.objects.get(user_id=request.user.id)
        user_applications = Application.objects.filter(applicant_id=user.user.id)
        all_listings = all_listings.filter(id__in=user_applications.values_list('listing_id', flat=True))

    elif applied_status == 'show_not_applied':
        user = Applicant.objects.get(user_id=request.user.id)
        user_applications = Application.objects.filter(applicant_id=user.user.id)
        applied_listing_ids = user_applications.values_list('listing_id', flat=True)
        all_listings = all_listings.exclude(id__in=applied_listing_ids)

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
        all_listings = all_listings.filter(company__name__icontains=company)

    if sort == 'pay_asc':
        all_listings = all_listings.order_by('salary_low')

    elif sort == 'pay_desc':
        all_listings = all_listings.order_by('salary_high')

    elif sort == 'due_date_asc':
        all_listings = all_listings.order_by('due_date')

    elif sort == 'due_date_desc':
        all_listings = all_listings.order_by('-due_date')

    elif sort == 'date_added_asc':
        all_listings = all_listings.order_by('date_added')

    elif sort == 'date_added_desc':
        all_listings = all_listings.order_by('-date_added')

    if category:
        category_id = Category.objects.get(field=category)
        all_listings = all_listings.filter(category=category_id)

    if employment_type == 'full_time':
        all_listings = all_listings.filter(employment_type_id=1)

    elif employment_type == 'part_time':
        all_listings = all_listings.filter(employment_type_id=2)

    elif employment_type == 'summer_job':
        all_listings = all_listings.filter(employment_type_id=3)

    all_listings = all_listings.filter(due_date__gte=datetime.date.today())

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


@login_required
def listing_detail(request: HttpRequest, lid: int) -> HttpResponse:
    listing = JobListing.objects.get(id=lid)
    user = Applicant.objects.get(user_id=request.user.id)
    application = Application.objects.filter(applicant=user, listing=listing).first()

    if application:
        context = {'listing': listing, 'application': application, 'applicant': user}
    else:
        context = {'listing': listing, 'applicant': user}

    return render(request, 'applicant/listing_detail.html', context)


@login_required
def choose_info(request: HttpRequest, lid: int) -> HttpResponse:
    applicant = Applicant.objects.get(user_id=request.user.id)
    listing = JobListing.objects.get(id=lid)

    if request.method == 'POST':
        print("POST REQUEST MADE")
        form = ApplicationForm(applicant, request.POST, request.FILES)
        if form.is_valid():
            step = request.POST.get('step', 'review')
            print("STEP: " + str(step))
            if step == 'review':
                form_data = {
                    'resume': form.cleaned_data['resume'],
                    'recommendations': form.cleaned_data['recommendations'],
                    'education': form.cleaned_data['educations'],
                    'work_experience': form.cleaned_data['experiences'],
                    'cover_letter': form.cleaned_data['cover_letter'],
                }
                return render(request, 'applicant/review.html',
                              {'form_data': form_data, 'form': form, 'listing': listing})
            elif step == 'final':
                print("GOT TO FINAL")
                # Final submission
                new_application = Application(
                    applicant=applicant, recruiter=listing.recruiter, date=datetime.date.today(),
                    listing=listing, status=Status.objects.get(id=1),
                    cover_letter=form.cleaned_data['cover_letter']
                )
                new_application.save()

                ApplicationResume(application=new_application, resume=form.cleaned_data['resume']).save()

                for education_item in form.cleaned_data['educations']:
                    ApplicationEducation(application=new_application, education=education_item).save()

                for experience_item in form.cleaned_data['experiences']:
                    ApplicationWorkExperience(application=new_application, work_experience=experience_item).save()

                for recommendation_item in form.cleaned_data['recommendations']:
                    ApplicationRecommendations(application=new_application, recommendation=recommendation_item).save()

                return render(request, 'applicant/listing_detail.html',
                              {'listing': listing, 'application': new_application})
        else:
            print("Form is invalid.")
            print(form.errors)
    else:
        form = ApplicationForm(applicant)

    return render(request, 'applicant/choose_info.html', {'form': form, 'listing': listing})




@login_required
def profile(request: HttpRequest) -> HttpResponse:
    user = Applicant.objects.get(user_id=request.user.id)
    experience_form_set = inlineformset_factory(Applicant, Experience, form=ExperienceForm, extra=1, can_delete=True)
    education_form_set = inlineformset_factory(Applicant, Education, form=EducationForm, extra=1, can_delete=True)
    resume_form_set = inlineformset_factory(Applicant, Resume, form=ResumeForm, extra=1, can_delete=True)
    recommendation_form_set = inlineformset_factory(Applicant, Recommendation, form=RecommendationForm, extra=1,
                                                    can_delete=True)

    if request.method == 'POST':
        applicant_form = ApplicantForm(request.POST, request.FILES, instance=user)
        experience_formset = experience_form_set(request.POST, instance=user)
        education_formset = education_form_set(request.POST, instance=user)
        resume_formset = resume_form_set(request.POST, request.FILES, instance=user)
        recommendation_formset = recommendation_form_set(request.POST, instance=user)
        if (applicant_form.is_valid() and experience_formset.is_valid() and education_formset.is_valid() and
                resume_formset.is_valid() and recommendation_formset.is_valid()):
            applicant_form.save()
            experience_formset.save()
            education_formset.save()
            resume_formset.save()
            recommendation_formset.save()
            user.completed_profile = True
            user.save()
            return redirect('applicant:listings')
    else:
        applicant_form = ApplicantForm(instance=user)
        experience_formset = experience_form_set(instance=user)
        education_formset = education_form_set(instance=user)
        resume_formset = resume_form_set(instance=user)
        recommendation_formset = recommendation_form_set(instance=user)

    return render(request, 'applicant/profile.html', {
        'form': applicant_form,
        'experience_formset': experience_formset,
        'education_formset': education_formset,
        'resume_formset': resume_formset,
        'recommendation_formset': recommendation_formset,
    })


@login_required
def applications(request: HttpRequest) -> HttpResponse:
    user = Applicant.objects.get(user_id=request.user.id)
    all_applications = Application.objects.filter(applicant_id=user.user.id)
    job_title = request.GET.get('job_title')
    if job_title:
        all_applications = all_applications.filter(listing__job_title__icontains=job_title)
    return render(request, 'applicant/applications.html', {'applications': all_applications})
