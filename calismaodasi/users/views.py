from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            kullanici = form.save()
            login(request, kullanici)
            return redirect("home")
    else: 
        form = UserCreationForm()
    return render(request, "calismaodasi/register.html", {"form": form})