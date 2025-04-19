from django.shortcuts import render
from .models import Paises, RolesUser
from .forms import RegistroUserForm
from django.shortcuts import render, redirect

# Create your views here.
def registrarUser(response):
    if response.method == "POST":
        form = RegistroUserForm(response.POST)
        if form.is_valid():
            form.save()
        return render(response, "registro-exitoso.html", {"form": form})
    else:
        form = RegistroUserForm()
        return render(response, "registro-exitoso.html", {"form": form}) 