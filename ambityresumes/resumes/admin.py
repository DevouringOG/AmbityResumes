from django.contrib import admin
from resumes.models import (
    Applicant,
    Education,
    Experience,
    Resume,
    Area,
    EducationLevel,
    ExperienceIndustry,
    ExperiencePosition,
    Currency,
    Folder,
)

admin.site.register(
    [
        Applicant,
        Education,
        Experience,
        Resume,
        Area,
        EducationLevel,
        ExperienceIndustry,
        ExperiencePosition,
        Currency,
        Folder,
    ]
)
