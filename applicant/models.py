from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.core.validators import RegexValidator


class Applicant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    street_name = models.CharField(max_length=100)
    house_number = models.CharField(max_length=100)
    country = CountryField()
    postal_code = models.CharField(max_length=13)
    applicant_image = models.ImageField(null=True, blank=True, upload_to='images/')
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    gender = models.CharField(max_length=25)
    city = models.CharField(max_length=85)
    ssn = models.CharField(max_length=10)
    completed_profile = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"Applicant: {self.user.first_name} {self.user.last_name}"

    class Meta:
        app_label = 'applicant'


class Education(models.Model):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    school = models.CharField(max_length=100)
    level = models.CharField(max_length=100)
    additional_info = models.TextField()
    location = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        app_label = 'applicant'

    def __str__(self) -> str:
        return f"School: {self.school} {self.level} From {self.start_date} to {self.end_date}"


class Resume(models.Model):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resumes/')

    class Meta:
        app_label = 'applicant'

    def __str__(self) -> str:
        return str(str(self.resume).strip("resumes/"))



class Experience(models.Model):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    main_responsibility = models.TextField()

    class Meta:
        app_label = 'applicant'

    def __str__(self) -> str:
        return f"{self.company_name}  as {self.role} - From {self.start_date} to {self.end_date}"


class Recommendation(models.Model):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=17, unique=True)
    company_name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    email = models.EmailField()
    can_be_contacted = models.BooleanField(default=True)

    class Meta:
        app_label = 'applicant'

    def __str__(self) -> str:
        return f"{self.name} from {self.company_name}"
