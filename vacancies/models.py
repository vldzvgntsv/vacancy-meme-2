from django.contrib.auth.models import User
from django.db import models
from django.db.models import CharField, DateField, ForeignKey, IntegerField, TextField, OneToOneField, ImageField

from conf.settings import MEDIA_COMPANY_IMAGE_DIR, MEDIA_SPECIALTY_IMAGE_DIR


class Company(models.Model):
    name = CharField(max_length=64)
    location = CharField(max_length=64)
    logo = ImageField(upload_to=MEDIA_COMPANY_IMAGE_DIR)
    description = TextField()
    employee_count = IntegerField()
    owner = OneToOneField(User, related_name='company', on_delete=models.SET_NULL, null=True)


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
