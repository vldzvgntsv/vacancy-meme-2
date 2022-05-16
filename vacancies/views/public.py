from django.db.models import Count, Q
from django.http import Http404
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView

from vacancies.forms import ApplicationForm
from vacancies.models import Company, Specialty, Vacancy


class HomePageView(TemplateView):
    template_name = 'vacancies/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['head_title'] = 'Главная'
        context['specialties'] = (
            Specialty.objects
            .annotate(num_vacancies=Count('vacancies'))
        )
        context['companies'] = (
            Company.objects
            .annotate(num_vacancies=Count('vacancies'))
        )
        return context


class ListVacanciesView(ListView):
    template_name = 'vacancies/vacancies.html'
    model = Vacancy

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['head_title'] = 'Вакансии'
        context['all_vacancies'] = True
        return context


class VacanciesCatView(ListView):
    template_name = 'vacancies/vacancies.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            specialty = Specialty.objects.get(code=self.kwargs['specialty']).title
        except Specialty.DoesNotExist:
            raise Http404
        context['head_title'] = specialty
        context['specialty'] = specialty
        context['all_vacancies'] = False
        return context

    def get_queryset(self):
        vacancy_queryset = Vacancy.objects.filter(specialty__code=self.kwargs['specialty'])
        return vacancy_queryset


class CompanyCardView(ListView):
    template_name = 'vacancies/company.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            company = Company.objects.get(id=self.kwargs['id'])
        except Company.DoesNotExist:
            raise Http404
        context['head_title'] = company.name
        context['company_name'] = company.name
        context['company_location'] = company.location
        context['company_logo'] = company.logo
        return context

    def get_queryset(self):
        vacancy_queryset = Vacancy.objects.filter(company__id=self.kwargs['id'])
        return vacancy_queryset


class SingleVacancyView(DetailView):
    template_name = 'vacancies/vacancy.html'
    model = Vacancy

    def post(self, request, **kwargs):
        application_form = ApplicationForm(request.POST)
        if not request.user.is_authenticated:
            return redirect('login')
        if application_form.is_valid():
            application_form.instance.vacancy = Vacancy.objects.get(id=self.kwargs['pk'])
            application_form.instance.user = request.user
            application_form.save()
            return redirect(request.path + 'send')
        return render(request, 'vacancies/form.html', context={'form': application_form})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['head_title'] = 'Вакансия ' + Vacancy.objects.get(id=self.kwargs['pk']).title
        context['form'] = ApplicationForm
        return context


class SendView(TemplateView):
    template_name = 'vacancies/sent.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['head_title'] = 'Отклик отправлен'
        return context


class SearchView(View):

    def get(self, request, **kwargs):
        query = request.GET.get('s')
        vacancies = Vacancy.objects.filter(
            Q(title__icontains=query) | Q(description__contains=query)
        )
        context = {
            'head_title': 'Поиск вакансий',
            'vacancies': vacancies,
            'query': query,
        }
        return render(request, 'vacancies/search.html', context=context)
