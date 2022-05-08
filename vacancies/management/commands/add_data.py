from django.core.management import BaseCommand

from vacancies.data import companies, jobs, specialties
from vacancies.models import Company, Specialty, Vacancy


class Command(BaseCommand):
    def handle(self, *args, **options):
        for company in companies:
            Company.objects.create(
                name=company['title'],
                location=company['location'],
                description=company['description'],
                employee_count=company['employee_count'],
            )

        for specialty in specialties:
            Specialty.objects.create(
                code=specialty['code'],
                title=specialty['title'],
            )

        for job in jobs:
            Vacancy.objects.create(
                title=job['title'],
                specialty=Specialty.objects.get(code=job['specialty']),
                company=Company.objects.get(id=int(job['company'])),
                skills=job['skills'],
                description=job['description'],
                salary_min=int(job['salary_from']),
                salary_max=int(job['salary_to']),
                published_at=job['posted'],
            )
