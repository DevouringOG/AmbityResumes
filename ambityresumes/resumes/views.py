from typing import Any
from django.db.models.query import QuerySet
from django.views import View
from django.views.generic import TemplateView, ListView
from django.http import HttpResponseRedirect
from resumes.models import Resume, Applicant, Area, Education, EducationLevel, ExperienceIndustry, Currency, ExperiencePosition, Experience
import requests
from django.apps import apps
import re
from transliterate import translit
from django.utils import timezone
from datetime import datetime



class UpdateDataView(View):
    MODELS_AND_URLS = {
        'EducationLevel': 'http://a0814722.xsph.ru/api/educationLevels',
        'ExperienceIndustry': 'http://a0814722.xsph.ru/api/experienceIndustry',
        'ExperiencePosition': 'http://a0814722.xsph.ru/api/experiencePosition',
        'Currency': 'http://a0814722.xsph.ru/api/currency',
    }
    API_KEY = 'Bxq7HZmXVDHVUW1d2X0J'

    def get(self, request, *args, **kwargs):
        headers = {'Api-key': self.API_KEY}

        response = requests.get("http://a0814722.xsph.ru/api/arias", headers=headers)
        for item_name in response.json():
            if item_name:
                if bool(re.search('[a-zA-Z]', item_name)):
                    item_name = translit(item_name, "ru")
                    print(item_name)
                Area.objects.get_or_create(name=item_name)

        for i, j in self.MODELS_AND_URLS.items():
            response = requests.get(j, headers=headers)
            model = apps.get_model("resumes", i)
            for item_name in response.json():
                if item_name:
                    model.objects.get_or_create(name=item_name)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))



class SearchResumesView(ListView):
    template_name = "resumes/search.html"
    context_object_name = "resumes"
    paginate_by = 50
    model = Resume

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["areas"] = Area.objects.all()
        context["education_levels"] = EducationLevel.objects.all()
        context["industrys"] = ExperienceIndustry.objects.all()
        context["positions"] = ExperiencePosition.objects.all()
        context["currencys"] = Currency.objects.all()
        context["today"] = (
            timezone.localdate()
            .strftime("%Y.%m.%d")
            .replace(".", "-")
        )
        return context

    def get_queryset(self):
        # Параметры фильтрации
        age_from = self.request.GET.get('age_from')
        age_to = self.request.GET.get('age_to')
        area = self.request.GET.get('area')
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        education_level = self.request.GET.get('education_level')
        experience_industry = self.request.GET.get('industry')
        gender = self.request.GET.get('gender')
        currency = self.request.GET.get('currency')
        salary_from = self.request.GET.get('salary_from')
        salary_to = self.request.GET.get('salary_to')
        total_experience = self.request.GET.get('total_experience')
        
        # Получаем резюме из API
        api_url = 'http://a0814722.xsph.ru/api/resume'
        headers = {'Api-key': 'Bxq7HZmXVDHVUW1d2X0J'}
        params = {}
        for key, value in self.request.GET.items():
            if value and key not in ["total_experience", "position", "date_from", "date_to"]:
                params[key] = value
                print(params[key])
            # if key in ["date_from", "date_to"]:
            #     params[key] = datetime.strptime(value, '%Y-%m-%d').isoformat()
            #     print(params[key])

        response = requests.get(api_url, headers=headers, params=params)

        if response.status_code == 200:
            print(200)
            api_resumes = response.json()
            # Создаем резюме в БД на основе ответа API
            for api_resume in api_resumes:
                education_data = api_resume.pop('education', {})
                experience_data = api_resume.get('experience', {})
                salary = api_resume.get("salary", {})
                
                # Проверяем, существует ли такой соискатель в БД
                applicant, created = Applicant.objects.get_or_create(
                    first_name=api_resume["first_name"],
                    last_name=api_resume["last_name"],
                    middle_name=api_resume["middle_name"],
                    age=api_resume["age"],
                    gender=api_resume["gender"] if api_resume["gender"] else "Не указан",
                    phone=api_resume["phone"],
                    email=api_resume["email"],
                    total_experience=api_resume["total_experience"],
                    area=translit(api_resume["area"], "ru"),
                )
                
                # Создаем или обновляем образование соискателя
                Education.objects.update_or_create(
                    applicant=applicant,
                    level=EducationLevel.objects.get(name=education_data["level"]) if education_data['level'] else None,
                    primary_name=education_data['primary_name'] if education_data['primary_name'] else None,
                    primary_organization=education_data['primary_organization'] if education_data['primary_organization'] else None,
                    primary_result=education_data['primary_result'] if education_data['primary_result'] else None,
                    primary_year=education_data['primary_year'] if education_data['primary_year'] else None,
                )
                
                start_date_str = experience_data['start']
                end_date_str = experience_data['end']

                # Преобразование строки даты в объект datetime
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d %H:%M:%S')
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d %H:%M:%S')

                # Преобразование обратно в строку в нужном формате
                start_date_formatted = start_date.strftime('%Y-%m-%d')
                end_date_formatted = end_date.strftime('%Y-%m-%d')

                area_inst = Area.objects.get_or_create(name=translit(experience_data["area"], "ru")),
                print(experience_data['industry'])
                Experience.objects.update_or_create(
                    applicant=applicant,
                    area=area_inst[0][0],
                    company=experience_data['company'],
                    start=start_date_formatted,
                    end=end_date_formatted,
                    industry=ExperienceIndustry.objects.get(name=experience_data['industry']) if experience_data['industry'] else None,
                    position=ExperiencePosition.objects.get(name=experience_data['position']) if experience_data['position'] else None,
                )
                
                # Создаем или обновляем резюме
                Resume.objects.update_or_create(
                    api_id=api_resume['id'],
                    defaults={
                        'applicant': applicant,
                        'certificate': api_resume['certificate'],
                        'salary_amount': salary['amount'],
                        'salary_currency': Currency.objects.get(name=salary['currency']),
                        'title': api_resume['title'],
                        'description': api_resume['resume'] if api_resume['resume'] else None,
                        "created_at": api_resume['created_at'],
                        "updated_at": api_resume['updated_at'],
                    }
                )
            
            # Фильтрация резюме в БД
            # Инициализация базового queryset
            queryset = Resume.objects.all()

            # Проверка и фильтрация по возрасту
            if age_from is not None:
                queryset = queryset.filter(applicant__age__gte=age_from)

            if age_to is not None:
                queryset = queryset.filter(applicant__age__lte=age_to)

            # Проверка и фильтрация по району
            if area is not None:
                queryset = queryset.filter(applicant__area__name=area)

            # Проверка и фильтрация по дате создания
            if date_from is not None:
                queryset = queryset.filter(created_at__gte=date_from)

            if date_to is not None:
                queryset = queryset.filter(created_at__lte=date_to)

            # Проверка и фильтрация по общему опыту
            if total_experience is not None:
                queryset = queryset.filter(applicant__total_experience__gte=total_experience)

            # Проверка и фильтрация по полу
            if gender is not None:
                queryset = queryset.filter(applicant__gender=gender)

            # Проверка и фильтрация по зарплате
            if salary_from is not None:
                queryset = queryset.filter(salary_amount__gte=salary_from)

            if salary_to is not None:
                queryset = queryset.filter(salary_amount__lte=salary_to)
            
            if education_level:
                queryset = queryset.filter(applicant__educations__level__name=education_level)
                
            if experience_industry:
                queryset = queryset.filter(experience__industry__name=experience_industry)
                
            if currency:
                queryset = queryset.filter(salary_currency__name=currency)
                
            return queryset.distinct()
        
        else:
            return Resume.objects.none()
