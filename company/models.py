from django.db import models
from utilities_static.models import Category, EmploymentType, Status
from django.contrib.auth.models import User
import datetime
from applicant.models import Applicant, Education, Resume, Recommendation, Experience


class Company(models.Model):
    name = models.CharField(max_length=100)
    ssn = models.CharField(max_length=15)
    phone_number = models.CharField(max_length=15, unique=True)
    info = models.TextField()
    location = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='images/')
    cover_image = models.ImageField(upload_to='cover_images/', default='cover_images/default_cover.webp')

    class Meta:
        app_label = 'company'

    def __str__(self) -> str:
        return self.name


class Recruiter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    company_ssn = models.CharField(max_length=15)

    class Meta:
        app_label = 'company'

    def __str__(self) -> str:
        return f"Recruiter: {self.user.first_name} {self.user.last_name}"


class JobListing(models.Model):
    id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    location = models.TextField()
    date_added = models.DateField(default=datetime.date.today)
    due_date = models.DateField(default="2025-01-01")
    job_title = models.CharField(max_length=100)
    salary_low = models.IntegerField()
    salary_high = models.IntegerField()
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    employment_type = models.ForeignKey(EmploymentType, on_delete=models.CASCADE)
    description = models.TextField()
    starting_date = models.DateField(default=datetime.date.today() + datetime.timedelta(days=60))

    class Meta:
        app_label = 'company'

    def __str__(self):
        return (f"{self.company} - {self.job_title} - {self.due_date} - {self.salary_low} $ - {self.salary_high} $ / "
                f"Per Year")


class Application(models.Model):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today)
    listing = models.ForeignKey(JobListing, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    models.UniqueConstraint(fields=['user', 'listing'], name='unique_application')
    cover_letter = models.TextField()

    class Meta:
        app_label = 'company'

    def __str__(self) -> str:
        return (f"{self.applicant.user.first_name} {self.applicant.user.last_name} {self.listing.company} "
                f"{self.listing.job_title} {self.status}")


class ApplicationEducation(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    education = models.ForeignKey(Education, on_delete=models.CASCADE)

    class Meta:
        app_label = 'company'

    def __str__(self) -> str:
        return (f"EDUCATION {self.application.listing.company} {self.application.listing.job_title} - "
                f"{self.application.applicant.user.first_name} {self.education}")


class ApplicationResume(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)

    class Meta:
        app_label = 'company'


class ApplicationRecommendations(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    recommendation = models.ForeignKey(Recommendation, on_delete=models.CASCADE)

    class Meta:
        app_label = 'company'

    def __str__(self) -> str:
        return (f"RECOMMENDATION {self.application.listing.company} {self.application.listing.job_title} -"
                f" {self.application.applicant.user.first_name} {self.recommendation.name}")


class ApplicationWorkExperience(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    work_experience = models.ForeignKey(Experience, on_delete=models.CASCADE)

    class Meta:
        app_label = 'company'

    def __str__(self) -> str:
        return (f"WORK EXPERIENCE {self.application.listing.company} {self.application.listing.job_title} -"
                f" {self.application.applicant.user.first_name} {self.work_experience}")
