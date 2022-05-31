from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View

from vacancies.forms import ResumeForm


class MyResumeStart(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, **kwargs):
        if hasattr(request.user, 'resume'):
            return redirect('my-resume-edit')
        context = {
            'head_title': 'Создание резюме',
        }
        return render(request, 'vacancies/resume-create.html', context=context)


class MyResumeCreate(LoginRequiredMixin, View):
    login_url = '/login/'

    def post(self, request, **kwargs):
        resume_form = ResumeForm(request.POST)
        if resume_form.is_valid():
            resume_form.instance.user = request.user
            resume_form.save()
            return redirect('my-resume-edit')
        context = {
            'head_title': 'Моe резюме',
            'form': resume_form,
        }
        return render(request, 'vacancies/resume-edit.html', context=context)

    def get(self, request, **kwargs):
        if hasattr(request.user, 'resume'):
            return redirect('my-resume-edit')
        context = {
            'head_title': 'Мое резюме',
            'form': ResumeForm(),
        }
        return render(request, 'vacancies/resume-edit.html', context=context)


class MyResumeEdit(LoginRequiredMixin, View):
    login_url = '/login/'

    def post(self, request, **kwargs):
        resume_form = ResumeForm(request.POST)
        if resume_form.is_valid():
            resume_form.instance.owner = request.user
            resume_form.save()
            return redirect('my-resume-edit')
        context = {
            'head_title': 'Моe резюме',
            'form': resume_form,
        }
        return render(request, 'vacancies/resume-edit.html', context=context)

    def get(self, request, **kwargs):
        if not hasattr(request.user, 'resume'):
            return redirect('my-resume-start')
        context = {
            'head_title': 'Мое резюме',
            'form': ResumeForm(instance=request.user.resume),
        }
        return render(request, 'vacancies/resume-edit.html', context=context)
