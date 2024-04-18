from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login
from django.views import View
from django.shortcuts import render, redirect

class AuthView(View):
    def get(self, request):
        login_form = AuthenticationForm()
        register_form = UserCreationForm()
        return render(request, 'users/auth.html', {'login_form': login_form, 'register_form': register_form})

    def post(self, request):
        if 'login_submit' in request.POST:
            form = AuthenticationForm(request=request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('some_redirect_view_name')  # Замените на имя вашего представления после входа
            else:
                login_form = AuthenticationForm(data=request.POST)
                register_form = UserCreationForm()
                return render(request, 'users/auth.html', {'login_form': login_form, 'register_form': register_form})
        elif 'register_submit' in request.POST:
            form = UserCreationForm(data=request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('some_redirect_view_name')  # Замените на имя вашего представления после регистрации
            else:
                login_form = AuthenticationForm()
                register_form = UserCreationForm(data=request.POST)
                return render(request, 'users/auth.html', {'login_form': login_form, 'register_form': register_form})
