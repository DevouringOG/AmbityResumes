from datetime import datetime
import os
import re

from django.apps import apps
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
)
import dotenv
import requests
from transliterate import translit

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


dotenv.load_dotenv(override=True)


class UpdateDataView(View):
    MODELS_AND_URLS = {
        "EducationLevel": "http://a0814722.xsph.ru/api/educationLevels",
        "ExperienceIndustry": "http://a0814722.xsph.ru/api/experienceIndustry",
        "ExperiencePosition": "http://a0814722.xsph.ru/api/experiencePosition",
        "Currency": "http://a0814722.xsph.ru/api/currency",
    }
    API_KEY = os.getenv("API_KEY")
    BASE_URL = os.getenv("API_URL")

    def fetch_and_create(self, model, url, headers):
        response = requests.get(url, headers=headers)
        for item_name in response.json():
            if item_name:
                if re.search("[a-zA-Z]", item_name):
                    item_name = translit(item_name, "ru")
                model.objects.get_or_create(name=item_name)

    def get(self, request, *args, **kwargs):
        headers = {"Api-key": self.API_KEY}

        self.fetch_and_create(Area, f"{self.BASE_URL}arias", headers)

        for model_name, url in self.MODELS_AND_URLS.items():
            model = apps.get_model("resumes", model_name)
            self.fetch_and_create(model, url, headers)

        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))


class SearchResumesView(ListView):
    template_name = "resumes/search.html"
    context_object_name = "resumes"
    paginate_by = 50
    model = Resume

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "areas": Area.objects.all(),
                "education_levels": EducationLevel.objects.all(),
                "industrys": ExperienceIndustry.objects.all(),
                "positions": ExperiencePosition.objects.all(),
                "currencys": Currency.objects.all(),
                "today": timezone.localdate().strftime("%Y-%m-%d"),
            },
        )
        return context

    def get_queryset(self):
        params = self.extract_params()
        api_resumes = self.get_api_resumes(params)
        self.save_to_db(api_resumes)
        return self.filter_resumes(params)

    def extract_params(self):
        params = {
            key: value for key, value in self.request.GET.items() if value
        }
        for key in ["total_experience", "position", "date_from", "date_to"]:
            params.pop(key, None)
        return params

    def get_api_resumes(self, params):
        api_url = "http://a0814722.xsph.ru/api/resume"
        headers = {"Api-key": "Bxq7HZmXVDHVUW1d2X0J"}
        response = requests.get(api_url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        return []

    def save_to_db(self, api_resumes):
        resumes_ids = Resume.objects.all().values_list("pk", flat=True)
        for api_resume in api_resumes:
            if api_resume["id"] not in resumes_ids:
                self.save_applicant(api_resume)
                self.save_education(api_resume)
                self.save_experience(api_resume)
                self.save_resume(api_resume)

    def save_applicant(self, api_resume):
        applicant_data = {
            "first_name": api_resume.get("first_name", None),
            "last_name": api_resume.get("last_name", None),
            "middle_name": api_resume.get("middle_name", None),
            "age": api_resume.get("age", None),
            "gender": api_resume.get("gender", "Не указан"),
            "phone": api_resume.get("phone", None),
            "email": api_resume.get("email", None),
            "total_experience": api_resume.get("total_experience", None),
            "area": translit(api_resume.get("area", ""), "ru"),
        }
        Applicant.objects.get_or_create(**applicant_data)

    def save_education(self, api_resume):
        education_data = api_resume.get("education", {})
        applicant = Applicant.objects.filter(
            first_name=api_resume.get("first_name", None),
            last_name=api_resume.get("last_name", None),
        ).first()
        if applicant:
            Education.objects.update_or_create(
                applicant=applicant,
                level=EducationLevel.objects.get_or_create(
                    name=education_data["level"],
                )[0]
                if education_data["level"]
                else None,
                primary_name=education_data.get("primary_name", None),
                primary_organization=education_data.get(
                    "primary_organization",
                    None,
                ),
                primary_result=education_data.get("primary_result", None),
                primary_year=education_data.get("primary_year", None),
            )

    def save_experience(self, api_resume):
        experience_data = api_resume.get("experience", {})
        applicant = Applicant.objects.filter(
            first_name=api_resume.get("first_name", None),
            last_name=api_resume.get("last_name", None),
        ).first()
        area, _ = (
            Area.objects.get_or_create(
                name=translit(experience_data["area"], "ru"),
            )
            if experience_data["area"]
            else None
        )
        if applicant:
            start_date = datetime.strptime(
                experience_data.get("start", ""),
                "%Y-%m-%d %H:%M:%S",
            )
            end_date = datetime.strptime(
                experience_data.get("end", ""),
                "%Y-%m-%d %H:%M:%S",
            )
            Experience.objects.update_or_create(
                applicant=applicant,
                area=area,
                company=experience_data.get("company", None),
                start=start_date.strftime("%Y-%m-%d"),
                end=end_date.strftime("%Y-%m-%d"),
                industry=ExperienceIndustry.objects.get_or_create(
                    name=experience_data["industry"],
                )[0]
                if experience_data["industry"]
                else None,
                position=ExperiencePosition.objects.get_or_create(
                    name=experience_data["position"],
                )[0]
                if experience_data["position"]
                else None,
            )

    def save_resume(self, api_resume):
        salary = api_resume.get("salary", {})
        applicant = Applicant.objects.filter(
            first_name=api_resume.get("first_name", None),
            last_name=api_resume.get("last_name", None),
        ).first()
        if applicant:
            Resume.objects.update_or_create(
                api_id=api_resume.get("id", None),
                defaults={
                    "applicant": applicant,
                    "certificate": api_resume.get("certificate", None),
                    "salary_amount": salary.get("amount", None),
                    "salary_currency": Currency.objects.get_or_create(
                        name=salary["currency"],
                    )[0]
                    if salary["currency"]
                    else None,
                    "title": api_resume.get("title", None),
                    "description": api_resume.get("resume", None),
                    "created_at": api_resume.get("created_at", None),
                    "updated_at": api_resume.get("updated_at", None),
                },
            )

    def filter_resumes(self, params):
        queryset = Resume.objects.select_related(
            "applicant",
            "salary_currency",
        )

        if "age_from" in params:
            queryset = queryset.filter(applicant__age__gte=params["age_from"])

        if "age_to" in params:
            queryset = queryset.filter(applicant__age__lte=params["age_to"])

        if "area" in params:
            queryset = queryset.filter(applicant__area=params["area"])

        if "date_from" in params:
            queryset = queryset.filter(created_at__gte=params["date_from"])

        if "date_to" in params:
            queryset = queryset.filter(created_at__lte=params["date_to"])

        if "total_experience" in params:
            queryset = queryset.filter(
                applicant__total_experience__gte=params["total_experience"],
            )

        if "gender" in params:
            queryset = queryset.filter(applicant__gender=params["gender"])

        if "salary_from" in params:
            queryset = queryset.filter(
                salary_amount__gte=params["salary_from"],
            )

        if "salary_to" in params:
            queryset = queryset.filter(salary_amount__lte=params["salary_to"])

        if "education_level" in params:
            queryset = queryset.filter(
                applicant__educations__level__name=params["education_level"],
            )

        if "industry" in params:
            queryset = queryset.filter(
                experience__industry__name=params["industry"],
            )

        if "currency" in params:
            queryset = queryset.filter(
                salary_currency__name=params["currency"],
            )

        return queryset.distinct()


class SaveFolderView(CreateView):
    model = Folder
    fields = ["name"]
    template_name = "your_template_name.html"
    success_url = reverse_lazy("users:account")

    def form_valid(self, form):
        folder = form.save(commit=False)
        folder.user = self.request.user

        resumes_ids_str = self.request.POST.get("resumes")
        resumes_ids = [
            int(id) for id in resumes_ids_str.split(",") if id.isdigit()
        ]
        resumes = Resume.objects.filter(id__in=resumes_ids)

        folder.save()
        folder.resumes.set(resumes)
        folder.save()

        return super().form_valid(form)


class FolderView(ListView):
    model = Resume
    context_object_name = "resumes"
    template_name = "resumes/folder.html"
    paginate_by = 50

    def get_queryset(self):
        folder = Folder.objects.get(pk=self.kwargs["folder_pk"])
        return folder.resumes.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        folder = Folder.objects.get(pk=self.kwargs["folder_pk"])
        context["folder"] = folder
        return context


# Я очень торопился не обращайте внимание на эту вьюшку
class ResumeView(DetailView):
    model = Resume
    template_name = "resumes/view.html"
    context_object_name = "resume"
    pk_url_kwarg = "resume_pk"

    def post(self, request, *args, **kwargs):
        resume = Resume.objects.get(pk=self.kwargs["resume_pk"])

        if "invite" in request.POST:
            status = resume.invite
            resume.invite = not status
            resume.save()

            invite_folder = Folder.objects.get(
                name="Приглашённые",
                user=request.user,
            )
            if status:
                invite_folder.resumes.remove(resume)
            else:
                invite_folder.resumes.add(resume)

        if "delete" in request.POST:
            status = resume.delete
            resume.delete = not status
            resume.save()

            delete_folder = Folder.objects.get(
                name="Удалённые",
                user=request.user,
            )
            main_folder = Folder.objects.get(pk=self.kwargs["folder_pk"])
            main_folder.resumes.remove(resume)
            if status:
                delete_folder.resumes.remove(resume)
            else:
                delete_folder.resumes.add(resume)

        if "favorite" in request.POST:
            status = resume.favorite
            resume.favorite = not status
            resume.save()

            favorite_folder = Folder.objects.get(
                name="Избранные",
                user=request.user,
            )
            if status:
                favorite_folder.resumes.remove(resume)
            else:
                favorite_folder.resumes.add(resume)

        return redirect(
            reverse_lazy(
                "resumes:folder",
                kwargs={"folder_pk": self.kwargs["folder_pk"]},
            ),
        )
