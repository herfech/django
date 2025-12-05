from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import CustomUserCreationForm

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Kayıt başarılı! Hoş geldiniz 🎉")
            return redirect("home")
        else:
            messages.error(request, "Kayıt başarısız. Lütfen formu kontrol edin.")
    else:
        form = CustomUserCreationForm()
    return render(request, "calismaodasi/register.html", {"form": form})