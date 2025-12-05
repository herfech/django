from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone
from datetime import datetime, date

from notifications.models import Notification

from .forms import ReservationForm
from .models import Reservation
from rooms.models import Room


@login_required
def create_reservation(request, room_pk):
    room = get_object_or_404(Room, pk=room_pk)
    
 
    context = {'form': ReservationForm(), 'room': room}
    
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            

            res_date = form.cleaned_data['date']
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']
            

            now = timezone.now().date()
            
            if res_date < now:
                messages.error(request, "Hata: Geçmiş bir tarih için rezervasyon yapamazsınız.") # Error: No puedes reservar para una fecha pasada.
                return render(request, 'create.html', context)
            

            conflict_exists = Reservation.objects.filter(
                room=room,
                date=res_date,

                end_time__gt=start_time, 

                start_time__lt=end_time
            ).exists()

            if conflict_exists:
                messages.error(request, "Hata: Seçilen saat aralığı başka bir rezervasyonla çakışıyor.") 
                return render(request, 'create.html', context)
            

            reservation = Reservation.objects.create(
                user=request.user,
                room=room,
                date=res_date,
                start_time=start_time,
                end_time=end_time,
            )
            

            Notification.create_reservation_notification(request.user, reservation.id)

            messages.success(request, f"Rezervasyon başarıyla oluşturuldu! Oda {room.name}.")
            return redirect('rooms:list') 
        

        else:
            context['form'] = form
            messages.error(request, "Hata: Formda eksik veya hatalı bilgi var.")
            return render(request, 'create.html', context)
            
    return render(request, 'create.html', context)


@login_required
def my_reservations(request):
    qs = Reservation.objects.filter(user=request.user).select_related('room').order_by('-date', '-start_time')
    return render(request, 'mine.html', {'reservations': qs})

