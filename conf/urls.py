"""conf URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path

from accounts.views import MySignupView, MyLoginView
from conf import settings
from vacancies.views import CompanyCardView, HomePageView, ListVacanciesView, SingleVacancyView, VacanciesCatView, \
    SendView, MyCompanyEdit, MyCompanyCreate, MyCompanyStart

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePageView.as_view(), name='main'),
    path('vacancies/', ListVacanciesView.as_view(), name='vacancies'),
    path('vacancies/cat/<str:specialty>/', VacanciesCatView.as_view(), name='vacancies-cat'),
    path('companies/<int:id>/', CompanyCardView.as_view(), name='company-card'),
    path('vacancies/<int:pk>/', SingleVacancyView.as_view(), name='single-vacancy'),
    path('vacancies/<int:pk>/send/', SendView.as_view(), name='send'),
    path('mycompany/letsstart/', MyCompanyStart.as_view(), name='my-company-start'),
    path('mycompany/create/', MyCompanyCreate.as_view(), name='my-company-create'),
    path('mycompany/', MyCompanyEdit.as_view(), name='my-company-edit'),
    path('register/', MySignupView.as_view(), name='register'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
