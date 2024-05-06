from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='landing'),
    path('choose', views.choose, name='choose'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('register', views.register, name='register'),
    path('companies', views.companies, name='companies'),
    path('company/<int:cid>', views.company_detail, name='company_detail'),
    path('listings', views.listings, name='listings'),
    path('listings/<int:lid>', views.listing_detail, name='listing_detail'),
    path('profile/<int:uid>', views.profile, name='profile'),
    path('profile/<int:uid>/applications', views.applications, name='applications'),
    path('profile/<int:uid>/listings', views.profile_listings, name='profile_listings'),
    path('profile/<int:uid>/listings/<int:lid>', views.profile_listing_detail, name='profile_listing_detail'),
    path('profile/<int:uid>/listings/<int:lid>/applicants', views.listing_applicants, name='listing_applicants'),
    path('profile/<int:uid>/listings/<int:lid>/applicants/<int:aid>', views.applicant_detail, name='applicant_detail'),
]
