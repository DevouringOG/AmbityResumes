from django.db import models


# Соискатель
class Applicant(models.Model):
    GENDER_CHOICES = [
        ("M", "Мужской"),
        ("F", "Женский"),
    ]

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    age = models.PositiveIntegerField()
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default="M",
    )
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField()
    total_experience = models.PositiveIntegerField()
    area = models.ForeignKey(
        "Area", on_delete=models.SET_NULL, null=True, blank=True
    )

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
    primary_name = models.CharField(max_length=255)
    primary_organization = models.CharField(max_length=255)
    primary_result = models.CharField(max_length=255)
    primary_year = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.applicant.last_name} {self.applicant.first_name} - {self.primary_name}"


# Опыт работы
class Experience(models.Model):
    applicant = models.ForeignKey(
        Applicant, related_name="experiences", on_delete=models.CASCADE
    )
    area = models.ForeignKey("Area", on_delete=models.SET_NULL, null=True)
    company = models.CharField(max_length=255)
    start = models.DateField()
    end = models.DateField()
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
    applicant = models.OneToOneField(Applicant, on_delete=models.CASCADE)
    certificate = models.URLField(blank=True, null=True)
    salary_amount = models.PositiveIntegerField()
    salary_currency = models.ForeignKey(
        "Currency", on_delete=models.SET_NULL, null=True
    )
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=2048)

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
    code = models.CharField(max_length=3)

    def __str__(self):
        return self.code