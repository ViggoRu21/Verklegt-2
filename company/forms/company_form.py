from django import forms
from company.models import Company, Recruiter, JobListing, Application, ApplicationEducation, ApplicationResume, \
    ApplicationRecommendations, ApplicationWorkExperience
import datetime
from django.utils import timezone


class companyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['company_name', 'company_ssn', 'phone_number', 'company_info', 'company_logo']


class RecruiterForm(forms.ModelForm):
    class Meta:
        model = Recruiter
        fields = ['user', 'company_ssn']
        widgets = {
            'company_ssn': forms.TextInput(attrs={'placeholder': 'Enter Company SSN'}),
        }


class JobListingForm(forms.ModelForm):
    model = JobListing
    fields = ['company', 'date_added', 'due_date', 'job_title', 'salary_low', 'salary_high', 'recruiter', 'category',
              'employment_type']
    widgets = {
        'date_added': forms.DateInput(format=('%Y-%m-%d'),
                                      attrs={'type': 'date', 'value': timezone.now().strftime("%Y-%m-%d")}),
        'due_date': forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'}),
        'job_title': forms.TextInput(attrs={'placeholder': 'Enter job title'}),
        'salary_low': forms.NumberInput(attrs={'min': 0, 'placeholder': 'Minimum salary'}),
        'salary_high': forms.NumberInput(attrs={'min': 0, 'placeholder': 'Maximum salary'}),
    }


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['applicant', 'recruiter', 'listing', 'status']


class ApplicationEducationForm(forms.ModelForm):
    pass


class ApplicationResumeForm(forms.ModelForm):
    pass


class ApplicationRecommendationsForm(forms.ModelForm):
    pass


class ApplicationWorkExperienceForm(forms.ModelForm):
    pass
