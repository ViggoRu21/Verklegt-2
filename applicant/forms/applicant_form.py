from django import forms
from applicant.models import Applicant, Education, Experience, Recommendation, Resume
from typing import Any
from datetime import date

from django import forms
from applicant.models import Applicant, Education, Experience, Recommendation, Resume
from typing import Any
from datetime import date


class ApplicantForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = Applicant
        fields = ['first_name', 'last_name', 'ssn', 'gender', 'applicant_image',  'phone_number',  'country', 'city',

                  'postal_code', 'street_name', 'house_number']
        widgets = {
            'applicant_image': forms.FileInput(attrs={'accept': 'image/*'}),
            'ssn': forms.TextInput(),
            'phone_number': forms.TextInput(),
            'gender': forms.Select(choices=[('', '-----'), ('Male', 'Male'), ('Female', 'Female'), ('Non-Binary','Non-Binary'), ('Other', 'Other'), ('Prefer not to say', 'Prefer not to say')]),
            'country': forms.Select(),
            'city': forms.TextInput(),
            'postal_code': forms.TextInput(),
            'street_name': forms.TextInput(),
            'house_number': forms.TextInput(),
        }

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(ApplicantForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name

    def save(self, *args: Any, **kwargs: Any) -> None:
        instance = super(ApplicantForm, self).save(*args, **kwargs)
        instance.user.first_name = self.cleaned_data.get('first_name')
        instance.user.last_name = self.cleaned_data.get('last_name')
        instance.user.save()
        return instance


class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['school', 'level', 'location', 'start_date', 'end_date', 'additional_info']
        exclude = ['applicant']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'additional_info': forms.Textarea(attrs={'class': 'forms_fix1'}),
        }


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = '__all__'
        exclude = ['applicant']


class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = '__all__'
        exclude = ['applicant']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'main_responsibility': forms.Textarea(attrs={'class': 'forms_fix1'}),
        }

    def validate_end_date(self) -> date:
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')
        if end_date < start_date:
            raise forms.ValidationError("End date should be after the start date.")
        return end_date


class RecommendationForm(forms.ModelForm):
    class Meta:
        model = Recommendation
        fields = '__all__'
        exclude = ['applicant']


class ApplicationForm(forms.Form):
    resume = forms.ModelChoiceField(queryset=Resume.objects.none())
    recommendations = forms.ModelMultipleChoiceField(queryset=Recommendation.objects.none(),
                                                     widget=forms.CheckboxSelectMultiple)
    educations = forms.ModelMultipleChoiceField(queryset=Education.objects.none(),
                                                widget=forms.CheckboxSelectMultiple)
    experiences = forms.ModelMultipleChoiceField(queryset=Experience.objects.none(),
                                                 widget=forms.CheckboxSelectMultiple)
    cover_letter = forms.CharField(widget=forms.Textarea)

    def __init__(self, applicant, *args, **kwargs):
        super().__init__(*args, **kwargs)

        resumes = Resume.objects.filter(applicant=applicant)
        recommendations = Recommendation.objects.filter(applicant=applicant)
        educations = Education.objects.filter(applicant=applicant)
        experiences = Experience.objects.filter(applicant=applicant)

        self.fields['resume'].queryset = resumes
        self.fields['recommendations'].queryset = recommendations
        self.fields['educations'].queryset = educations
        self.fields['experiences'].queryset = experiences

