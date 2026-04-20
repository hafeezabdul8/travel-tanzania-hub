from django.core.mail import send_mail
from django.conf import settings

def send_hotel_booking_confirmation(booking, user_email):
    """
    Send booking confirmation email to user
    """
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
        [user_email],
        fail_silently=True,
    )
