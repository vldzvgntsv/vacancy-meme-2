from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View

from vacancies.forms import VacancyForm
from vacancies.models import Vacancy, Application


class MyVacanciesList(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, **kwargs):
        if not hasattr(request.user, 'company'):
            return redirect('my-company-start')
        my_vacancies = Vacancy.objects.filter(company=request.user.company)
        context = {
            'head_title': 'Вакансии компании',
            'my_vacancies': my_vacancies,
        }
        return render(request, 'vacancies/vacancy-list.html', context=context)


class MyVacancyCreate(LoginRequiredMixin, View):
    login_url = '/login/'

    def post(self, request, **kwargs):
        vacancy_form = VacancyForm(request.POST)
        if vacancy_form.is_valid():
            vacancy_form.instance.company = request.user.company
            vacancy_form.save()
            return redirect('/')
        context = {
            'head_title': 'Моя компания',
            'form': VacancyForm(instance=vacancy_form),
        }
        return render(request, 'vacancies/vacancy-edit.html', context=context)

    def get(self, request, **kwargs):
        if not hasattr(request.user, 'company'):
            return redirect('my-company-start')
        context = {
            'head_title': 'Создание вакансии',
            'form': VacancyForm(),
        }
        return render(request, 'vacancies/vacancy-edit.html', context=context)


class MyVacancyEdit(LoginRequiredMixin, View):
    login_url = '/login/'

    def post(self, request, **kwargs):
        try:
            vacancy = Vacancy.objects.get(id=kwargs['id'])
        except Vacancy.DoesNotExist:
            return redirect('my-vacancies-list')
        vacancy_form = VacancyForm(request.POST, instance=vacancy)
        if vacancy_form.is_valid():
            vacancy_form.save()
            return redirect('my-vacancy-edit', kwargs['id'])
        context = {
            'head_title': 'Редактирование вакансии',
            'form': vacancy_form,
        }
        return render(request, 'vacancies/vacancy-edit.html', context=context)

    def get(self, request, **kwargs):
        if not hasattr(request.user, 'company'):
            return redirect('my-company-start')
        try:
            vacancy = Vacancy.objects.get(id=kwargs['id'])
        except Vacancy.DoesNotExist:
            return redirect('my-vacancy-create')
        if vacancy not in Vacancy.objects.filter(company=request.user.company):
            return redirect('my-vacancy-create')
        applications = Application.objects.filter(vacancy_id=kwargs['id'])
        context = {
            'head_title': 'Редактирование вакансии',
            'form': VacancyForm(instance=vacancy),
            'applications': applications,
        }
        return render(request, 'vacancies/vacancy-edit.html', context=context)
