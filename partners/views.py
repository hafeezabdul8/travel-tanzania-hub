from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Sum, Count, Q
from datetime import datetime, timedelta
from .models import Partner, PartnerPayout, PartnerNotification
from hotels.models import Booking, Hotel
from tourism.models import TourPackage, TourBooking, TouristAttraction

def is_partner(user):
    """Check if user is a registered partner"""
    return hasattr(user, 'partner_profile')

@login_required
def become_partner(request):
    """Partner registration form"""
    
    # Check if already a partner
    if hasattr(request.user, 'partner_profile'):
        messages.info(request, 'You are already registered as a partner!')
        return redirect('partner_dashboard')
    
    if request.method == 'POST':
        # Process partner registration
        # (We'll create this form in templates)
        business_name = request.POST.get('business_name')
        business_type = request.POST.get('business_type')
        contact_person = request.POST.get('contact_person')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        
        # Create partner profile
        partner = Partner.objects.create(
            user=request.user,
            business_name=business_name,
            business_type=business_type,
            contact_person=contact_person,
            phone=phone,
            email=email,
            address=address,
            city=city,
            status='pending'
        )
        
        messages.success(request, 
            'Partner registration submitted successfully! Our team will review your application.'
        )
        return redirect('partner_dashboard')
    
    return render(request, 'partners/become_partner.html')

@login_required
@user_passes_test(is_partner)
def partner_dashboard(request):
    """Partner's main dashboard"""
    
    partner = request.user.partner_profile
    
    # Get statistics
    stats = {
        'total_earnings': partner.total_earnings,
        'pending_payout': partner.pending_payout,
        'total_paid': partner.total_paid,
        'approved_listings': partner.get_approved_listings_count(),
        'active_bookings': partner.get_active_bookings_count(),
    }
    
    # Recent bookings based on business type
    recent_bookings = []
    if partner.business_type == 'hotel':
        hotels = Hotel.objects.filter(partner=request.user)
        recent_bookings = Booking.objects.filter(
            hotel__in=hotels
        ).select_related('user', 'hotel').order_by('-created_at')[:10]
    
    elif partner.business_type in ['tour_operator', 'attraction']:
        tour_packages = TourPackage.objects.filter(partner=request.user)
        recent_bookings = TourBooking.objects.filter(
            tour_package__in=tour_packages
        ).select_related('user', 'tour_package').order_by('-created_at')[:10]
    
    # Recent payouts
    recent_payouts = partner.payouts.all()[:5]
    
    # Unread notifications
    notifications = partner.notifications.filter(is_read=False)[:10]
    
    context = {
        'partner': partner,
        'stats': stats,
        'recent_bookings': recent_bookings,
        'recent_payouts': recent_payouts,
        'notifications': notifications,
    }
    
    return render(request, 'partners/dashboard.html', context)

# In partners/views.py - partner_bookings function
@login_required
@user_passes_test(is_partner)
def partner_bookings(request):
    """View all bookings for partner's listings"""
    partner = request.user.partner_profile
    bookings = []
    total_bookings = 0
    confirmed_bookings = 0
    pending_bookings = 0
    total_revenue = 0

    if partner.business_type == 'hotel':
        hotels = Hotel.objects.filter(partner=request.user)
        bookings = Booking.objects.filter(
            hotel__in=hotels
        ).select_related('user', 'hotel').order_by('-created_at')
        
        # Calculate counts
        total_bookings = bookings.count()
        confirmed_bookings = bookings.filter(status='confirmed').count()
        pending_bookings = bookings.filter(status='pending').count()
        
        # Calculate total revenue (partner's share)
        for booking in bookings.filter(status='confirmed'):
            total_revenue += float(booking.hotel_amount or 0)
    
    elif partner.business_type in ['tour_operator', 'attraction']:
        tour_packages = TourPackage.objects.filter(partner=request.user)
        bookings = TourBooking.objects.filter(
            tour_package__in=tour_packages
        ).select_related('user', 'tour_package').order_by('created_at')
        
        # Calculate counts
        total_bookings = bookings.count()
        confirmed_bookings = bookings.filter(status='confirmed').count()
        pending_bookings = bookings.filter(status='pending').count()
        
        # Calculate total revenue
        for booking in bookings.filter(status='confirmed'):
            booking_amount = float(booking.total_amount or 0)
            commission = float(booking.platform_commission or 0)
            total_revenue += booking_amount - commission

    context = {
        'partner': partner,
        'bookings': bookings,
        'total_bookings': total_bookings,
        'confirmed_bookings': confirmed_bookings,
        'pending_bookings': pending_bookings,
        'total_revenue': total_revenue,
    }

    return render(request, 'partners/bookings.html', context)
# partners/views.py - partner_earnings function
@login_required
@user_passes_test(is_partner)
def partner_earnings(request):
    """View earnings and commission reports"""
    partner = request.user.partner_profile
    
    # Initialize variables
    monthly_earnings = []
    recent_transactions = []
    max_earning = 0
    
    # Calculate monthly earnings for last 6 months
    for i in range(6):
        month_start = datetime.now().date().replace(day=1) - timedelta(days=30*i)
        month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        earnings = 0
        commission = 0
        
        if partner.business_type == 'hotel':
            month_bookings = Booking.objects.filter(
                hotel__partner=request.user,
                created_at__date__range=[month_start, month_end],
                status='confirmed'
            )
            # Calculate partner's earnings (hotel_amount)
            earnings_result = month_bookings.aggregate(
                total=Sum('hotel_amount')
            )
            earnings = earnings_result['total'] or 0
            
            # Calculate platform commission
            commission_result = month_bookings.aggregate(
                total=Sum('platform_commission')
            )
            commission = commission_result['total'] or 0
            
        elif partner.business_type in ['tour_operator', 'attraction']:
            month_bookings = TourBooking.objects.filter(
                tour_package__partner=request.user,
                created_at__date__range=[month_start, month_end],
                status='confirmed'
            )
            # Calculate partner's earnings (total_amount - commission)
            total_result = month_bookings.aggregate(
                total=Sum('total_amount')
            )
            total_amount = total_result['total'] or 0
            
            commission_result = month_bookings.aggregate(
                total=Sum('platform_commission')
            )
            commission = commission_result['total'] or 0
            
            earnings = total_amount - commission
        
        # Calculate net earnings
        net_earnings = float(earnings)
        
        monthly_earnings.append({
            'month': month_start.strftime('%b %Y'),
            'earnings': net_earnings,
            'commission': float(commission),
            'net': net_earnings,
        })
        
        # Track maximum for chart scaling
        if net_earnings > max_earning:
            max_earning = net_earnings
    
    # Get recent transactions (payouts)
    recent_transactions = partner.payouts.all()[:10]
    
    context = {
        'partner': partner,
        'monthly_earnings': monthly_earnings,
        'max_earning': max_earning,
        'recent_transactions': recent_transactions,
    }
    
    # In partners/views.py
    for month_data in monthly_earnings:
        if max_earning > 0:
            month_data['percentage'] = (month_data['earnings'] / max_earning) * 100
    else:
        month_data['percentage'] = 0

    return render(request, 'partners/earnings.html', context)
@login_required
@user_passes_test(is_partner)
# partners/views.py
def partner_listings(request):
    """Manage partner's listings (hotels, tours, attractions)"""
    partner = request.user.partner_profile
    
    # Calculate partner's percentage
    partner_receives = 100 - float(partner.commission_rate)
    
    hotels = []
    tour_packages = []
    attractions = []

    if partner.business_type == 'hotel':
        hotels = Hotel.objects.filter(partner=request.user)
    elif partner.business_type == 'tour_operator':
        tour_packages = TourPackage.objects.filter(partner=request.user)
    elif partner.business_type == 'attraction':
        attractions = TouristAttraction.objects.filter(partner=request.user)

    context = {
        'partner': partner,
        'partner_receives': partner_receives,  # Add this
        'hotels': hotels,
        'tour_packages': tour_packages,
        'attractions': attractions,
    }

    return render(request, 'partners/listings.html', context)

@login_required
@user_passes_test(is_partner)
def partner_settings(request):
    """Partner account settings"""
    
    partner = request.user.partner_profile
    
    if request.method == 'POST':
        # Update partner information
        partner.business_name = request.POST.get('business_name', partner.business_name)
        partner.contact_person = request.POST.get('contact_person', partner.contact_person)
        partner.phone = request.POST.get('phone', partner.phone)
        partner.email = request.POST.get('email', partner.email)
        partner.address = request.POST.get('address', partner.address)
        partner.save()
        
        messages.success(request, 'Settings updated successfully!')
        return redirect('partner_settings')
    
    context = {
        'partner': partner,
    }
    
    return render(request, 'partners/settings.html', context)

@login_required
@user_passes_test(is_partner)
def mark_notification_read(request, notification_id):
    """Mark notification as read"""
    
    notification = get_object_or_404(
        PartnerNotification, 
        id=notification_id, 
        partner=request.user.partner_profile
    )
    notification.is_read = True
    notification.save()
    
    return JsonResponse({'success': True})

# Admin Views for Partner Management
@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_partner_management(request):
    """Admin view for managing all partners"""
    
    partners = Partner.objects.all()
    pending_count = partners.filter(status='pending').count()
    
    # Statistics
    stats = {
        'total_partners': partners.count(),
        'pending_approvals': pending_count,
        'approved_partners': partners.filter(status='approved').count(),
        'total_earnings': partners.aggregate(Sum('total_earnings'))['total_earnings__sum'] or 0,
        'pending_payouts': partners.aggregate(Sum('pending_payout'))['pending_payout__sum'] or 0,
    }
    
    context = {
        'partners': partners,
        'stats': stats,
    }
    
    return render(request, 'partners/admin_management.html', context)

# Add to partners/views.py

@login_required
@user_passes_test(is_partner)
def add_hotel(request):
    """Add new hotel for partner"""
    partner = request.user.partner_profile
    
    if partner.business_type != 'hotel':
        messages.error(request, 'You are not registered as a hotel owner.')
        return redirect('partner_listings')
    
    if request.method == 'POST':
        try:
            # Get form data
            name = request.POST.get('name')
            city = request.POST.get('city')
            address = request.POST.get('address')
            description = request.POST.get('description')
            price_per_night = request.POST.get('price_per_night')
            available_rooms = request.POST.get('available_rooms')
            stars = request.POST.get('stars', 3)
            
            # Create hotel
            hotel = Hotel.objects.create(
                name=name,
                city=city,
                address=address,
                description=description,
                price_per_night=price_per_night,
                available_rooms=available_rooms,
                stars=stars,
                partner=request.user,  # Link to partner
                wifi=request.POST.get('wifi') == 'on',
                pool=request.POST.get('pool') == 'on',
                restaurant=request.POST.get('restaurant') == 'on',
                parking=request.POST.get('parking') == 'on',
                commission_percentage=partner.commission_rate,  # Use partner's commission rate
                is_approved=False  # Needs admin approval
            )
            
            messages.success(request, f'Hotel "{name}" added successfully! It will be visible after admin approval.')
            return redirect('partner_listings')
            
        except Exception as e:
            messages.error(request, f'Error adding hotel: {str(e)}')
    
    return redirect('partner_listings')