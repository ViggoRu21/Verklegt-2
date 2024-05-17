from django.urls import path
from company import views

app_name = 'company'


urlpatterns = [
    path('login_page', views.login_page, name='login_page'),
    path('login_view', views.login_view, name='login_view'),
    path('logout', views.logout_view, name='logout'),
    path('register_page', views.register_page, name='register_page'),
    path('register_view', views.register_view, name='register_view'),
    path('forgot', views.forgot, name='forgot'),
    path('company', views.company_detail, name='company_detail'),
    path('listings', views.listings, name='listings'),
    path('listings/<int:lid>', views.listing_detail, name='listing_detail'),
    path('profile', views.profile, name='profile'),
    path('profilelistings', views.profile_listings, name='profile_listings'),
    path('profilelistings/<int:lid>', views.profile_listing_detail, name='profile_listing_detail'),
    path('profilelistings/<int:lid>/applicants', views.listing_applicants, name='listing_applicants'),
    path('profile/listings/<int:lid>/applicants/<int:aid>', views.applicant_detail, name='applicant_detail'),
]
