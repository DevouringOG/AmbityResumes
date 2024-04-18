from django.views import View
from django.views.generic import TemplateView


class SearchResumes(TemplateView):
    template_name = "resumes/search.html"


# class SearchResumes(View):
#     template_name = "resumes/search.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["areas"] = # http://a0814722.xsph.ru/api/arias
#         context["types"] = # http://a0814722.xsph.ru/api/experienceIndustry
#         context["positions"] = ... # http://a0814722.xsph.ru/api/experiencePosition
#         context["education_levels"] = # http://a0814722.xsph.ru/api/educationLevels
#         context["currencys"] = # http://a0814722.xsph.ru/api/currency
#         return context
