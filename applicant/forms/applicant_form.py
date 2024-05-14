from django import forms
from applicant.models import Applicant, Education, Experience, Recommendation


class ApplicantForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = Applicant
        fields = ['applicant_image','first_name', 'last_name', 'ssn', 'gender', 'phone_number',  'country', 'city',
                  'postal_code', 'street_name', 'house_number']
        widgets = {
            'applicant_image': forms.FileInput(attrs={'accept': 'image/*'}),
            'ssn': forms.TextInput(),
            'phone_number': forms.TextInput(),
            'gender': forms.Select(choices=[('Male', 'Male'), ('Female', 'Female'), ('Non-Binary', 'Non-Binary')]),  # Use a Select widget for gender
            'country': forms.Select(),
            'city': forms.TextInput(),
            'postal_code': forms.TextInput(),
            'street_name': forms.TextInput(),
            'house_number': forms.TextInput()
        }

    def __init__(self, *args, **kwargs):
        super(ApplicantForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name

    def save(self, *args, **kwargs):
        instance = super(ApplicantForm, self).save(*args, **kwargs)
        instance.user.first_name = self.cleaned_data.get('first_name')
        instance.user.last_name = self.cleaned_data.get('last_name')
        instance.user.save()
        return instance


class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['applicant', 'school', 'level', 'additional_info', 'location', 'start_date', 'end_date']
        exclude = ['id']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'additional_info': forms.TextInput(attrs={'type': 'text'}),
        }


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['applicant', 'school', 'level', 'additional_info', 'location', 'start_date', 'end_date']
        exclude = ['id']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'additional_info': forms.TextInput(attrs={'type': 'text'}),
        }


class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['applicant', 'company_name', 'start_date', 'end_date', 'main_responsibility']

    def validate_end_date(self):
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')
        if end_date < start_date:
            raise forms.ValidationError("End date should be after the start date.")
        return end_date


class RecommendationForm(forms.ModelForm):
    class Meta:
        model = Recommendation
        fields = ['applicant', 'name', 'phone_number', 'company_name']
