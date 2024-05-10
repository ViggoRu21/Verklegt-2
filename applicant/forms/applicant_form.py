from django import forms
from applicant.models import Applicant, Education, Experience, Recommendation


class ApplicantForm(forms.ModelForm):
    first = forms.CharField(max_length=30)
    last = forms.CharField(max_length=30)
    class Meta:
        # TODO finna út hvernig við bætum við inn í user upplýsingar eins og first name, last name af því að það er ekki í þessum klara
        model = Applicant
        fields = ['user', 'applicant_image']
        widgets = {
            'applicant_page': forms.FileInput(attrs={'accept': 'image/*'}),
        }
    #def update_user(self):
        #user = Applicant.user
        #user.first_name = first
        #user.last_name = last



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
    pass


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
