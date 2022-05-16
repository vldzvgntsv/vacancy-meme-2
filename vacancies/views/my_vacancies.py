from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render
from django.views import View

from vacancies.forms import VacancyForm
from vacancies.models import Vacancy, Application


class MyVacanciesList(View):

    def get(self, request, **kwargs):
        try:
            company = request.user.company
        except ObjectDoesNotExist:
            return redirect('my-company-start')
        my_vacancies = Vacancy.objects.filter(company=company)
        context = {
            'head_title': 'Вакансии компании',
            'my_vacancies': my_vacancies,
        }
        return render(request, 'vacancies/vacancy-list.html', context=context)


class MyVacancyCreate(View):

    def post(self, request, **kwargs):
        vacancy_form = VacancyForm(request.POST)
        if vacancy_form.is_valid():
            vacancy_form.instance.company = request.user.company
            vacancy_form.instance.published_at = datetime.today()
            vacancy_form.save()
            return redirect('/')
        context = {
            'head_title': 'Моя компания',
            'form': VacancyForm(instance=vacancy_form),
        }
        return render(request, 'vacancies/vacancy-edit.html', context=context)

    def get(self, request, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        try:
            request.user.company
        except ObjectDoesNotExist:
            return redirect('my-company-start')
        context = {
            'head_title': 'Создание вакансии',
            'form': VacancyForm(),
        }
        return render(request, 'vacancies/vacancy-edit.html', context=context)


class MyVacancyEdit(View):

    def post(self, request, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        try:
            vacancy = Vacancy.objects.get(id=kwargs['id'])
        except Vacancy.DoesNotExist:
            return redirect('my-vacancies-list')
        vacancy_form = VacancyForm(request.POST, instance=vacancy)
        if vacancy_form.is_valid():
            vacancy_form.save()
            return redirect('/')
        context = {
            'head_title': 'Редактирование вакансии',
            'form': vacancy_form,
        }
        return render(request, 'vacancies/vacancy-edit.html', context=context)

    def get(self, request, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        try:
            company = request.user.company
        except ObjectDoesNotExist:
            return redirect('my-company-start')
        try:
            vacancy = Vacancy.objects.get(id=kwargs['id'])
        except Vacancy.DoesNotExist:
            return redirect('my-vacancy-create')
        if vacancy not in Vacancy.objects.filter(company=company):
            return redirect('my-vacancy-create')
        applications = Application.objects.filter(vacancy_id=kwargs['id'])
        context = {
            'head_title': 'Редактирование вакансии',
            'form': VacancyForm(instance=vacancy),
            'applications': applications,
        }
        return render(request, 'vacancies/vacancy-edit.html', context=context)
