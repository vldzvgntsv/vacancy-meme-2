from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from vacancies.models import Application, Company, Vacancy


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ('written_username', 'written_phone', 'written_cover_letter')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Откликнуться'))


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('name', 'location', 'description', 'employee_count')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Сохранить'))


class VacancyForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = ('title', 'specialty', 'skills', 'salary_min', 'salary_max', 'description')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Сохранить'))
