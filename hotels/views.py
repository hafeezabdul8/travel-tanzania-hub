from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Hotel, RoomType, Booking
from datetime import datetime, timedelta

def hotel_list(request):
    city = request.GET.get('city', '')
    search = request.GET.get('search', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    
    hotels = Hotel.objects.all()
    
    # Apply filters
    if city:
        hotels = hotels.filter(city=city)
    
    if search:
        hotels = hotels.filter(
            Q(name__icontains=search) |
            Q(address__icontains=search) |
            Q(description__icontains=search)
        )
    
    if min_price:
        hotels = hotels.filter(price_per_night__gte=min_price)
    
    if max_price:
        hotels = hotels.filter(price_per_night__lte=max_price)
    
    # Group by city for display
    dar_hotels = hotels.filter(city='DAR')
    aru_hotels = hotels.filter(city='ARU')
    zan_hotels = hotels.filter(city='ZAN')
    
    context = {
        'hotels': hotels,
        'dar_hotels': dar_hotels,
        'aru_hotels': aru_hotels,
        'zan_hotels': zan_hotels,
        'selected_city': city,
        'search_query': search,
    }
    return render(request, 'hotels/list.html', context)

def hotel_detail(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    room_types = hotel.room_types.all()
    
    # Default dates (tomorrow to 3 days later)
    tomorrow = datetime.now().date() + timedelta(days=1)
    check_out_default = tomorrow + timedelta(days=3)
    
    context = {
        'hotel': hotel,
        'room_types': room_types,
        'default_check_in': tomorrow.strftime('%Y-%m-%d'),
        'default_check_out': check_out_default.strftime('%Y-%m-%d'),
    }
    return render(request, 'hotels/detail.html', context)
from utils.emails import send_hotel_booking_confirmation

@login_required
def book_hotel(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    
    if request.method == 'POST':
        # parse booking form data
        check_in_str = request.POST.get('check_in')
        check_out_str = request.POST.get('check_out')
        guests = request.POST.get('guests', '1')
        special_requests = request.POST.get('special_requests', '').strip()

        if not check_in_str or not check_out_str:
            messages.error(request, 'Please provide check-in and check-out dates.')
            return redirect('hotel_detail', hotel_id=hotel_id)

        try:
            check_in_date = datetime.strptime(check_in_str, '%Y-%m-%d').date()
            check_out_date = datetime.strptime(check_out_str, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, 'Invalid date format. Use YYYY-MM-DD.')
            return redirect('hotel_detail', hotel_id=hotel_id)

        if check_out_date <= check_in_date:
            messages.error(request, 'Check-out must be after check-in.')
            return redirect('hotel_detail', hotel_id=hotel_id)

        try:
            guests = int(guests)
            if guests < 1:
                guests = 1
        except ValueError:
            guests = 1

        nights = (check_out_date - check_in_date).days
        total_price = nights * (hotel.price_per_night or 0)

        # Create booking
        booking = Booking.objects.create(
            user=request.user,
            hotel=hotel,
            check_in=check_in_date,
            check_out=check_out_date,
            guests=guests,
            total_price=total_price,
            special_requests=special_requests,
            status='pending'
        )

        # Send confirmation email
        try:
            send_hotel_booking_confirmation(booking)
            messages.success(request, f'Booking created successfully! Confirmation email sent to {request.user.email}')
        except Exception as e:
            messages.warning(request, f'Booking created but email failed to send. Please contact support.')
            print(f"Email error: {e}")

        return redirect('booking_confirmation', booking_id=booking.id)

    return redirect('hotel_detail', hotel_id=hotel_id)
@login_required
def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, 'hotels/confirmation.html', {'booking': booking})

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'hotels/my_bookings.html', {'bookings': bookings})