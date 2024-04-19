from django.db import models
from django.contrib.auth.models import User


# Соискатель
class Applicant(models.Model):
    GENDER_CHOICES = [
        ("Мужчина", "Мужчина"),
        ("Женщина", "Женщина"),
        ("Не указан", "Не указан"),
    ]

    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    age = models.PositiveIntegerField(null=True)
    gender = models.CharField(
        max_length=15,
        choices=GENDER_CHOICES,
        default="Мужчина",
        null = True,
    )
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(null=True)
    total_experience = models.PositiveIntegerField(null=True)
    area = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.middle_name or ''}"


# Образование соискателя
class Education(models.Model):
    applicant = models.ForeignKey(
        Applicant, related_name="educations", on_delete=models.CASCADE
    )
    level = models.ForeignKey(
        "EducationLevel", on_delete=models.SET_NULL, null=True
    )
    primary_name = models.CharField(max_length=255, null=True)
    primary_organization = models.CharField(max_length=255, null=True)
    primary_result = models.CharField(max_length=255, null=True)
    primary_year = models.PositiveIntegerField(null=True)

    def __str__(self):
        return f"{self.applicant.last_name} {self.applicant.first_name} - {self.primary_name}"


# Опыт работы
class Experience(models.Model):
    applicant = models.ForeignKey(
        Applicant, related_name="experiences", on_delete=models.CASCADE
    )
    area = models.ForeignKey("Area", on_delete=models.SET_NULL, null=True)
    company = models.CharField(max_length=255, null=True)
    start = models.DateField(null=True)
    end = models.DateField(null=True)
    industry = models.ForeignKey(
        "ExperienceIndustry", on_delete=models.SET_NULL, null=True
    )
    position = models.ForeignKey(
        "ExperiencePosition", on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        return f"{self.applicant.last_name} {self.applicant.first_name} - {self.position}"


# Резюме
class Resume(models.Model):
    api_id = models.IntegerField(unique=True)
    applicant = models.OneToOneField(Applicant, on_delete=models.CASCADE)
    certificate = models.URLField(blank=True, null=True)
    salary_amount = models.PositiveIntegerField(null=True)
    salary_currency = models.ForeignKey(
        "Currency", on_delete=models.SET_NULL, null=True
    )
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    description = models.CharField(max_length=2048, null=True)

    def __str__(self):
        return f"{self.applicant.last_name} {self.applicant.first_name} - {self.title}"


# Регион
class Area(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# Уровнь образования
class EducationLevel(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# Отрасль компании
class ExperienceIndustry(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# Должность компании
class ExperiencePosition(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# Код валют
class Currency(models.Model):
    name = models.CharField(max_length=3)

    def __str__(self):
        return self.name


# Папка
class Folder(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_create = models.DateField(auto_now=True)
    resumes = models.ManyToManyField(Resume)
