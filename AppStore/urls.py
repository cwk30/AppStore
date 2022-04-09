"""AppStore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

import app.views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', app.views.index, name='index'),
    path('parent', app.views.parentloginregister, name='Parents Portal'),
    path('nanny',app.views.nannyloginregister, name='Nannies Portal'),
    path("accounts/", include("django.contrib.auth.urls")),
    path('add', app.views.add, name='add'),
    path('view/<str:id>', app.views.view, name='view'),
    path('edit/<str:id>', app.views.edit, name='edit'),
    path('nanny_application', app.views.nanny_application, name='Application'),
    path('nanny_page', app.views.nanny_page, name='Nanny Hub'),
    path('nanny_bookings', app.views.nanny_bookings, name='Nanny Bookings'),
    path('nanny_opportunities', app.views.nanny_opportunities, name='Opportunities'),
    path('nanny_profile_page', app.views.nanny_profile_page, name='Nanny Profile Page'),
    path('nanny_requests', app.views.nanny_requests, name='Requests'),
    path('parent_browse_sitters', app.views.parents_browse_sitters, name='Browse Sitters'),
    path('parent_make_offer', app.views.parent_make_offer, name='Make an Offer'),
    path('parent_offers', app.views.parent_offers, name='Offers'),
    path('parent_page', app.views.parent_page, name='Parent Hub'),
    path('parent_profile', app.views.parent_profile, name='Parent Profile Page'),
    path('parent_bookings', app.views.parent_bookings, name='Parent Bookings'),
    path('view_applicants', app.views.view_applicants, name='View Applicants'),
    path('nanny_profile_update', app.views.nanny_profile_update, name='Nanny Profile Update'),
    path('nanny_availability_update', app.views.nanny_availability_update, name='Nanny Availability Update'),
    path('parent_profile_update', app.views.parent_profile_update, name='Parent Profile Update'),
    path('elements', app.views.elements, name='Elements'),
    path('index', app.views.index, name='Index 1'),
    path('index2', app.views.index2, name='Index 2'),
    # path('parentcreatejob', app.views.parentcreatejob, name='parentcreatejob'),
    path('nannyscheduleadd', app.views.nannyscheduleadd, name='nannyscheduleadd'),
    path('nannyscheduleview', app.views.nannyscheduleview, name='nannyscheduleview'),
    # path('nannybrowsejobs', app.views.nannybrowsejobs, name='nannybrowsejobs'),
    # path('parentsbrowsenannies', app.views.parentsbrowsenannies, name='parentsbrowsenannies'),
    path('jobview/<str:id>', app.views.jobview, name='jobview'),
    path('nannyview/<str:id>', app.views.nannyview, name='nannyview'),
    # path('nannyedit', app.views.nannyedit, name='nannyedit'),
    path('nannyreqs', app.views.nannyreqs, name='nannyreqs')

]
