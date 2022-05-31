from django.contrib.auth.models import User
from django.db import models
from django.db.models import (
    CharField, DateField, ForeignKey, IntegerField, TextField,
    OneToOneField, ImageField,
)

from conf.settings import MEDIA_COMPANY_IMAGE_DIR, MEDIA_SPECIALTY_IMAGE_DIR


class Company(models.Model):
    name = CharField(max_length=64)
    location = CharField(max_length=64)
    logo = ImageField(upload_to=MEDIA_COMPANY_IMAGE_DIR)
    description = TextField()
    employee_count = IntegerField()
    owner = OneToOneField(User, related_name='company', on_delete=models.CASCADE, null=True)


class Specialty(models.Model):
    code = CharField(max_length=32, unique=True)
    title = CharField(max_length=32)
    picture = ImageField(upload_to=MEDIA_SPECIALTY_IMAGE_DIR)


class Vacancy(models.Model):
    title = CharField(max_length=64)
    specialty = ForeignKey(Specialty, related_name='vacancies', on_delete=models.CASCADE, null=True)
    company = ForeignKey(Company, related_name='vacancies', on_delete=models.CASCADE, null=True)
    skills = CharField(max_length=128)
    description = TextField()
    salary_min = IntegerField()
    salary_max = IntegerField()
    published_at = DateField(auto_now_add=True)


class Application(models.Model):
    written_username = CharField(max_length=16)
    written_phone = CharField(max_length=12)
    written_cover_letter = TextField()
    vacancy = ForeignKey(Vacancy, related_name="applications", on_delete=models.CASCADE, null=True)
    user = ForeignKey(User, related_name="applications", on_delete=models.CASCADE, null=True)


class Resume(models.Model):
    STATUS_CHOICES = [
        ('N', 'Не ищу работу'),
        ('L', 'Рассматриваю предложения'),
        ('Y', 'Ищу работу')
    ]
    GRADE_CHOICES = [
        ('INT', 'Стажер'),
        ('JUN', 'Джуниор'),
        ('MID', 'Миддл'),
        ('SEN', 'Сеньор'),
        ('LED', 'Лид'),
    ]
    user = OneToOneField(User, related_name='resume', on_delete=models.CASCADE, null=True)
    name = CharField(max_length=32)
    surname = CharField(max_length=32)
    status = CharField(max_length=1, choices=STATUS_CHOICES, default='Y')
    salary = IntegerField()
    specialty = CharField(max_length=64)
    grade = CharField(max_length=3, choices=GRADE_CHOICES, default='JUN')
    education = CharField(max_length=256)
    experience = TextField()
    portfolio = CharField(max_length=256)
