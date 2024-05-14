from django import forms
from applicant.models import Applicant, Education, Experience, Recommendation, Resume


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
        fields = ['school', 'level', 'additional_info', 'location', 'start_date', 'end_date']
        exclude = ['applicant']
        widgets = {
            'start_date': forms.DateInput(attrs={'class': 'datepicker'}),
            'end_date': forms.DateInput(attrs={'class': 'datepicker'}),
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
            'start_date': forms.DateInput(attrs={'class': 'datepicker'}),
            'end_date': forms.DateInput(attrs={'class': 'datepicker'}),
        }

    def validate_end_date(self):
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