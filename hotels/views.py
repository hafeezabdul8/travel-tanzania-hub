from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Hotel, RoomType, Booking
from datetime import datetime, timedelta
from rest_framework import viewsets, permissions, generics, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .serializers import *

# ========== EMAIL FUNCTION (ADD THIS AT THE TOP) ==========
def send_hotel_booking_confirmation(booking):
    """
    Send booking confirmation email to user
    """
    try:
        from django.core.mail import send_mail
        from django.conf import settings
        
        subject = f'AFCON 2027 - Booking Confirmation for {booking.hotel.name}'
        message = f'''
        Dear {booking.user.username},

        Your booking at {booking.hotel.name} has been confirmed!

        Booking Details:
        ----------------
        Booking ID: #{booking.id}
        Hotel: {booking.hotel.name}
        Check-in: {booking.check_in}
        Check-out: {booking.check_out}
        Guests: {booking.guests}
        Total Price: ${booking.total_price}

        Thank you for choosing AFCON 2027 Hotels!
        
        Best regards,
        AFCON 2027 Team
        '''
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [booking.user.email],
            fail_silently=True,
        )
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False

# ========== VIEW FUNCTIONS ==========
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


# ========== API VIEWSETS ==========
# Hotel ViewSet
class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all().order_by('-stars', 'price_per_night')
    serializer_class = HotelSerializer
    
    def get_serializer_class(self):
        if self.action == 'list':
            return HotelListSerializer
        return HotelSerializer
    
    def get_queryset(self):
        queryset = Hotel.objects.all()
        
        # Filter by city
        city = self.request.query_params.get('city', None)
        if city:
            queryset = queryset.filter(city=city)
        
        # Filter by price range
        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)
        if min_price:
            queryset = queryset.filter(price_per_night__gte=min_price)
        if max_price:
            queryset = queryset.filter(price_per_night__lte=max_price)
        
        # Search by name
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(name__icontains=search)
        
        return queryset
    
    @action(detail=True, methods=['get'])
    def room_types(self, request, pk=None):
        hotel = self.get_object()
        room_types = hotel.room_types.all()
        serializer = RoomTypeSerializer(room_types, many=True)
        return Response(serializer.data)


# Booking Views
@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def user_bookings(request):
    if request.method == 'GET':
        bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def booking_detail(request, pk):
    try:
        booking = Booking.objects.get(pk=pk, user=request.user)
    except Booking.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = BookingSerializer(booking)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = BookingSerializer(booking, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        booking.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Authentication Views
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_api(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    if user:
        token, created = Token.objects.get_or_create(user=user)
        serializer = UserSerializer(user)
        return Response({
            'token': token.key,
            'user': serializer.data
        })
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_api(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email', '')
    
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = User.objects.create_user(username=username, password=password, email=email)
    token = Token.objects.create(user=user)
    
    # Create chat profile
    from chatbot.models import ChatProfile
    ChatProfile.objects.create(user=user)
    
    serializer = UserSerializer(user)
    return Response({
        'token': token.key,
        'user': serializer.data
    }, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_profile(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)