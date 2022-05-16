from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render
from django.views import View

from vacancies.forms import CompanyForm


class MyCompanyStart(View):

    def get(self, request, **kwargs):
        try:
            if request.user.company:
                return redirect('my-company-edit')
        except ObjectDoesNotExist:
            pass
        context = {
            'head_title': 'Создание компании',
        }
        return render(request, 'vacancies/company-start.html', context=context)


class MyCompanyCreate(View):

    def post(self, request, **kwargs):
        company_form = CompanyForm(request.POST)
        if company_form.is_valid():
            company_form.instance.owner = request.user
            company_form.save()
            return redirect('/')
        context = {
            'head_title': 'Моя компания',
            'form': CompanyForm(instance=company_form),
        }
        return render(request, 'vacancies/company-edit.html', context=context)

    def get(self, request, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        try:
            if request.user.company:
                return redirect('my-company-edit')
        except ObjectDoesNotExist:
            pass
        context = {
            'head_title': 'Моя компания',
            'form': CompanyForm(),
        }
        return render(request, 'vacancies/company-edit.html', context=context)


class MyCompanyEdit(View):

    def post(self, request, **kwargs):
        company_form = CompanyForm(request.POST, instance=request.user.company)
        if company_form.is_valid():
            company_form.save()
            return redirect('/')
        context = {
            'head_title': 'Моя компания',
            'form': company_form,
        }
        return render(request, 'vacancies/company-edit.html', context=context)

    def get(self, request, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        try:
            company = request.user.company
        except ObjectDoesNotExist:
            return redirect('my-company-start')
        context = {
            'head_title': 'Моя компания',
            'form': CompanyForm(instance=company),
        }
        return render(request, 'vacancies/company-edit.html', context=context)
