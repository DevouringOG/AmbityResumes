from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView

from resumes.models import Folder


class AuthView(View):
    """
    Представление для аутентификации пользователей.
    """

    def get(self, request):
        login_form = AuthenticationForm()
        register_form = UserCreationForm()
        return render(
            request,
            "users/auth.html",
            {"login_form": login_form, "register_form": register_form},
        )

    def post(self, request):
        """
        Обрабатывает данные форм входа и регистрации.
        """
        if "login_submit" in request.POST:
            form = AuthenticationForm(request=request, data=request.POST)
            if form.is_valid():
                user = self.authenticate_and_login(request, form.cleaned_data)
                if user:
                    return redirect(reverse_lazy("resumes:search"))
            else:
                return self.render_forms(
                    request,
                    AuthenticationForm(data=request.POST),
                    UserCreationForm(),
                )

        elif "register_submit" in request.POST:
            form = UserCreationForm(data=request.POST)
            if form.is_valid():
                form.save()
                user = self.authenticate_and_login(
                    request,
                    form.cleaned_data,
                    reg=True,
                )
                if user:
                    self.create_default_folders(user)
                    return redirect(reverse_lazy("resumes:search"))
            else:
                return self.render_forms(
                    request,
                    AuthenticationForm(),
                    UserCreationForm(data=request.POST),
                )

        return HttpResponseRedirect(reverse_lazy("users:auth"))

    def authenticate_and_login(self, request, cleaned_data, reg=False):
        """
        Аутентификация пользователя и вход в систему.
        """
        username = cleaned_data["username"]
        password = cleaned_data["password" if not reg else "password1"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return user
        return None

    def create_default_folders(self, user):
        """
        Создает стандартные папки для нового пользователя.
        """
        for folder_name in ["Приглашённые", "Удалённые", "Избранные"]:
            Folder.objects.create(name=folder_name, user=user)

    def render_forms(self, request, login_form, register_form):
        """
        Отображает формы входа и регистрации с переданными данными.
        """
        return render(
            request,
            "users/auth.html",
            {"login_form": login_form, "register_form": register_form},
        )


class AccountView(ListView):
    """
    Представление для отображения папок пользователя.
    """

    template_name = "users/account.html"
    context_object_name = "folders"
    model = Folder
    paginate_by = 6

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)
