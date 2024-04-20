from django.contrib import admin

from resumes.models import (
    Applicant,
    Area,
    Currency,
    Education,
    EducationLevel,
    Experience,
    ExperienceIndustry,
    ExperiencePosition,
    Folder,
    Resume,
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
    ],
)
