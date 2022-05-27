from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View

from vacancies.forms import CompanyForm


class MyCompanyStart(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, **kwargs):
        if hasattr(request.user, 'company'):
            return redirect('my-company-edit')
        context = {
            'head_title': 'Создание компании',
        }
        return render(request, 'vacancies/company-start.html', context=context)


class MyCompanyCreate(LoginRequiredMixin, View):
    login_url = '/login/'

    def post(self, request, **kwargs):
        company_form = CompanyForm(request.POST, request.FILES)
        if company_form.is_valid():
            company_form.instance.owner = request.user
            company_form.save()
            return redirect('my-company-edit')
        context = {
            'head_title': 'Моя компания',
            'form': CompanyForm(instance=company_form),
        }
        return render(request, 'vacancies/company-edit.html', context=context)

    def get(self, request, **kwargs):
        if hasattr(request.user, 'company'):
            return redirect('my-company-edit')
        context = {
            'head_title': 'Моя компания',
            'form': CompanyForm(),
        }
        return render(request, 'vacancies/company-edit.html', context=context)


class MyCompanyEdit(LoginRequiredMixin, View):
    login_url = '/login/'

    def post(self, request, **kwargs):
        company_form = CompanyForm(request.POST, request.FILES, instance=request.user.company)
        if company_form.is_valid():
            company_form.save()
            return redirect('my-company-edit')
        context = {
            'head_title': 'Моя компания',
            'form': company_form,
        }
        return render(request, 'vacancies/company-edit.html', context=context)

    def get(self, request, **kwargs):
        if not hasattr(request.user, 'company'):
            return redirect('my-company-start')
        context = {
            'head_title': 'Моя компания',
            'form': CompanyForm(instance=request.user.company),
        }
        return render(request, 'vacancies/company-edit.html', context=context)
