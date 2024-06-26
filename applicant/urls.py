from django.urls import path
from applicant import views

app_name = 'applicant'

urlpatterns = [
    path('login_page', views.login_page, name='login_page'),
    path('login_view', views.login_view, name='login_view'),
    path('logout', views.logout_user, name='logout'),
    path('register_page', views.register_page, name='register_page'),
    path('register_view', views.register_view, name='register_view'),
    path('companies', views.companies, name='companies'),
    path('company/<int:cid>', views.company_detail, name='company_detail'),
    path('listings', views.listings, name='listings'),
    path('listings/<int:lid>', views.listing_detail, name='listing_detail'),
    path('choose_info/<int:lid>', views.choose_info, name='choose_info'),
    path('profile', views.profile, name='profile'),
    path('profile/applications', views.applications, name='applications')
]
