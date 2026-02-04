from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.urls import reverse

def send_hotel_booking_confirmation(booking):
    """Send hotel booking confirmation email"""
    subject = f"✅ Hotel Booking Confirmed - #{booking.id:06d} - AFCON 2027"
    
    # Generate booking URL
    booking_url = f"http://yourdomain.com{reverse('booking_confirmation', args=[booking.id])}"
    chatbot_url = f"http://yourdomain.com{reverse('chatbot')}"
    
    # Prepare context
    context = {
        'booking': booking,
        'booking_url': booking_url,
        'chatbot_url': chatbot_url,
    }
    
    # Render HTML email
    html_content = render_to_string('emails/hotel_booking_confirmation.html', context)
    text_content = strip_tags(html_content)  # Plain text version
    
    # Create email
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[booking.user.email],
        cc=['bookings@afcon2027.tz'],  # Optional: CC to admin
        reply_to=['support@afcon2027.tz'],
    )
    
    # Attach HTML version
    email.attach_alternative(html_content, "text/html")
    
    # Send email
    try:
        email.send(fail_silently=False)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def send_tour_booking_confirmation(booking):
    """Send tour booking confirmation email"""
    subject = f"✅ Tour Booking Confirmed - #{booking.id:06d} - AFCON 2027"
    
    # Generate URLs
    booking_url = f"http://yourdomain.com{reverse('tour_booking_confirmation', args=[booking.id])}"
    
    context = {
        'booking': booking,
        'booking_url': booking_url,
    }
    
    html_content = render_to_string('emails/tour_booking_confirmation.html', context)
    text_content = strip_tags(html_content)
    
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[booking.user.email],
        cc=['tours@afcon2027.tz'],
        reply_to=['tours-support@afcon2027.tz'],
    )
    
    email.attach_alternative(html_content, "text/html")
    
    try:
        email.send(fail_silently=False)
        return True
    except Exception as e:
        print(f"Error sending tour booking email: {e}")
        return False

def send_booking_cancellation(booking, booking_type='hotel'):
    """Send booking cancellation email"""
    if booking_type == 'hotel':
        subject = f"❌ Hotel Booking Cancelled - #{booking.id:06d}"
        template = 'emails/hotel_booking_cancellation.html'
    else:
        subject = f"❌ Tour Booking Cancelled - #{booking.id:06d}"
        template = 'emails/tour_booking_cancellation.html'
    
    context = {'booking': booking}
    html_content = render_to_string(template, context)
    text_content = strip_tags(html_content)
    
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[booking.user.email],
    )
    
    email.attach_alternative(html_content, "text/html")
    
    try:
        email.send(fail_silently=False)
        return True
    except Exception as e:
        print(f"Error sending cancellation email: {e}")
        return False