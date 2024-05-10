from django import forms
from company.models import Company, Recruiter, JobListing, Application, ApplicationEducation, ApplicationResume, ApplicationRecommendations, ApplicationWorkExperience


class companyForm(forms.ModelForm):
    pass

class RecruiterForm(forms.ModelForm):
    pass

class JobListingForm(forms.ModelForm):
    pass

class ApplicationForm(forms.ModelForm):
    pass

class ApplicationEducationForm(forms.ModelForm):
    pass

class ApplicationResumeForm(forms.ModelForm):
    pass

class ApplicationRecommendationsForm(forms.ModelForm):
    pass

class ApplicationWorkExperienceForm(forms.ModelForm):
    pass