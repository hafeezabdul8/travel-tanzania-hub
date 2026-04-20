from decimal import Decimal
import json

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Sum, Count, Q
from django.core.paginator import Paginator
from datetime import datetime, timedelta
from .models import Partner, PartnerPayout, PartnerNotification, PartnerImage
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
        
        # Update coordinates
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        if latitude and longitude:
            partner.latitude = Decimal(latitude)
            partner.longitude = Decimal(longitude)
        
        partner.save()
        
        messages.success(request, 'Settings updated successfully!')
        return redirect('partners:partner_settings')
    
    context = {
        'partner': partner,
    }
    
    return render(request, 'partners/settings.html', context)
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

# ============ PUBLIC VIEWS (For Users to See Partners) ============

# Add these to your partner_list and partner_detail views

def partner_list(request):
    """Public page showing all approved partners"""
    
    partners = Partner.objects.filter(status='approved')
    
    # Get filter parameters
    category = request.GET.get('category', '')
    city = request.GET.get('city', '')
    search = request.GET.get('search', '')
    
    # Apply filters
    if category:
        partners = partners.filter(business_type=category)
    
    if city:
        partners = partners.filter(city=city)
    
    if search:
        partners = partners.filter(
            Q(business_name__icontains=search) |
            Q(description__icontains=search) |
            Q(city__icontains=search)
        )
    
    # Prefetch images for each partner to avoid N+1 queries
    partners = partners.prefetch_related('images')
    
    # Add primary image to each partner
    for partner in partners:
        partner.primary_logo = partner.images.filter(image_type='logo', is_primary=True).first()
        if not partner.primary_logo:
            partner.primary_logo = partner.images.filter(image_type='logo').first()
        if not partner.primary_logo:
            partner.primary_logo = partner.images.filter(is_approved=True).first()
    
    # Pagination
    paginator = Paginator(partners, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get counts for filters
    category_counts = {}
    for cat, label in Partner.BUSINESS_TYPES:
        category_counts[cat] = Partner.objects.filter(status='approved', business_type=cat).count()
    
    city_counts = {}
    for city_code, city_name in [('DAR', 'Dar es Salaam'), ('ARU', 'Arusha'), ('ZAN', 'Zanzibar')]:
        city_counts[city_code] = Partner.objects.filter(status='approved', city=city_code).count()
    
    context = {
        'partners': page_obj,
        'categories': Partner.BUSINESS_TYPES,
        'category_counts': category_counts,
        'city_counts': city_counts,
        'selected_category': category,
        'selected_city': city,
        'search_query': search,
    }
    return render(request, 'partners/partner_list.html', context)


def partner_detail(request, partner_id):
    """Public page showing detailed partner profile"""
    
    partner = get_object_or_404(Partner, id=partner_id, status='approved')
    
    # Get all images for this partner
    all_images = partner.images.filter(is_approved=True)
    
    # Get images by type
    logo_images = all_images.filter(image_type='logo')
    cover_images = all_images.filter(image_type='cover')
    interior_images = all_images.filter(image_type='interior')
    product_images = all_images.filter(image_type='product')
    team_images = all_images.filter(image_type='team')
    
    # Get primary logo and cover
    primary_logo = logo_images.filter(is_primary=True).first() or logo_images.first()
    primary_cover = cover_images.filter(is_primary=True).first() or cover_images.first()
    
    # Get partner's listings based on business type
    hotels = []
    tour_packages = []
    attractions = []
    
    if partner.business_type == 'hotel':
        hotels = Hotel.objects.filter(partner=partner.user, is_approved=True)[:10]
    elif partner.business_type == 'tour_operator':
        tour_packages = TourPackage.objects.filter(partner=partner.user)[:10]
    elif partner.business_type == 'attraction':
        attractions = TouristAttraction.objects.filter(partner=partner.user)[:10]
    
    # Get similar partners in same city
    similar_partners = Partner.objects.filter(
        status='approved',
        city=partner.city,
        business_type=partner.business_type
    ).exclude(id=partner.id)[:4]
    
    # Prefetch images for similar partners
    for similar in similar_partners:
        similar.primary_logo = similar.images.filter(image_type='logo', is_primary=True).first()
        if not similar.primary_logo:
            similar.primary_logo = similar.images.filter(image_type='logo').first()
    
    context = {
        'partner': partner,
        'all_images': all_images,
        'logo_images': logo_images,
        'cover_images': cover_images,
        'interior_images': interior_images,
        'product_images': product_images,
        'team_images': team_images,
        'primary_logo': primary_logo,
        'primary_cover': primary_cover,
        'hotels': hotels,
        'tour_packages': tour_packages,
        'attractions': attractions,
        'similar_partners': similar_partners,
    }
    return render(request, 'partners/partner_detail.html', context)

def partner_by_category(request, category):
    """Filter partners by category"""
    partners = Partner.objects.filter(status='approved', business_type=category)
    
    paginator = Paginator(partners, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    category_name = dict(Partner.BUSINESS_TYPES).get(category, category)
    
    context = {
        'partners': page_obj,
        'category_name': category_name,
        'category_slug': category,
    }
    return render(request, 'partners/partner_by_category.html', context)


def partner_by_city(request, city):
    """Filter partners by city"""
    partners = Partner.objects.filter(status='approved', city=city)
    
    paginator = Paginator(partners, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    city_names = {
        'DAR': 'Dar es Salaam',
        'ARU': 'Arusha',
        'ZAN': 'Zanzibar',
    }
    
    context = {
        'partners': page_obj,
        'city_name': city_names.get(city, city),
        'city_code': city,
    }
    return render(request, 'partners/partner_by_city.html', context)


def partner_search(request):
    """AJAX search endpoint for partners"""
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    city = request.GET.get('city', '')
    
    partners = Partner.objects.filter(status='approved')
    
    if query:
        partners = partners.filter(
            Q(business_name__icontains=query) |
            Q(description__icontains=query)
        )
    
    if category:
        partners = partners.filter(business_type=category)
    
    if city:
        partners = partners.filter(city=city)
    
    results = []
    for partner in partners[:20]:
        results.append({
            'id': partner.id,
            'business_name': partner.business_name,
            'business_type': partner.get_business_type_display(),
            'city': partner.get_city_display(),
            'phone': partner.phone,
        })
    
    return JsonResponse({'results': results, 'count': len(results)})


# ============ USER BOOKING VIEWS ============

@login_required
def book_partner_service(request, partner_id):
    """User books a service from a partner"""
    partner = get_object_or_404(Partner, id=partner_id, status='approved')
    
    if request.method == 'POST':
        service_type = request.POST.get('service_type')
        service_id = request.POST.get('service_id')
        booking_date = request.POST.get('booking_date')
        guests = request.POST.get('guests', 1)
        special_requests = request.POST.get('special_requests', '')
        
        # Create booking record (you need a PartnerBooking model)
        # For now, just show success message
        
        messages.success(request, f'Booking request sent to {partner.business_name}! They will contact you shortly.')
        return redirect('partners:partner_detail', partner_id=partner_id)
    
    # GET request - show booking form
    context = {
        'partner': partner,
    }
    return render(request, 'partners/book_partner.html', context)


@login_required
def my_partner_bookings(request):
    """User's bookings with partners"""
    # You need a PartnerBooking model for this
    # For now, just show placeholder
    context = {
        'bookings': [],
    }
    return render(request, 'partners/my_bookings.html', context)


@login_required
def cancel_partner_booking(request, booking_id):
    """Cancel a partner booking"""
    # You need a PartnerBooking model for this
    messages.success(request, 'Booking cancelled successfully.')
    return redirect('partners:my_partner_bookings')

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os

@login_required
@user_passes_test(is_partner)
def partner_images(request):
    """Manage partner's images"""
    partner = request.user.partner_profile
    images = partner.images.all()
    
    # Get counts by type
    image_counts = {
        'logo': images.filter(image_type='logo').count(),
        'cover': images.filter(image_type='cover').count(),
        'interior': images.filter(image_type='interior').count(),
        'product': images.filter(image_type='product').count(),
        'team': images.filter(image_type='team').count(),
    }
    
    context = {
        'partner': partner,
        'images': images,
        'image_counts': image_counts,
    }
    return render(request, 'partners/images.html', context)


@login_required
@user_passes_test(is_partner)
def add_partner_image(request):
    """Add new image for partner"""
    partner = request.user.partner_profile
    
    if request.method == 'POST':
        image_type = request.POST.get('image_type')
        title = request.POST.get('title', '')
        description = request.POST.get('description', '')
        is_primary = request.POST.get('is_primary') == 'on'
        
        # Handle uploaded file
        uploaded_file = request.FILES.get('image')
        image_url = request.POST.get('image_url', '')
        
        if uploaded_file:
            # Validate file type
            allowed_types = ['image/jpeg', 'image/png', 'image/jpg', 'image/gif', 'image/webp']
            if uploaded_file.content_type not in allowed_types:
                messages.error(request, 'Please upload a valid image file (JPEG, PNG, GIF, or WEBP).')
                return redirect('partners:partner_images')
            
            # Validate file size (max 5MB)
            if uploaded_file.size > 5 * 1024 * 1024:
                messages.error(request, 'Image size should be less than 5MB.')
                return redirect('partners:partner_images')
        
        # Create image record
        image = PartnerImage.objects.create(
            partner=partner,
            image=uploaded_file if uploaded_file else None,
            image_url=image_url if image_url else None,
            image_type=image_type,
            title=title,
            description=description,
            is_primary=is_primary,
            is_approved=True
        )
        
        # If this is set as primary, unset other primary images of same type
        if is_primary:
            PartnerImage.objects.filter(
                partner=partner, 
                image_type=image_type, 
                is_primary=True
            ).exclude(id=image.id).update(is_primary=False)
        
        messages.success(request, 'Image uploaded successfully! It will appear after admin approval.')
        return redirect('partners:partner_images')
    
    return redirect('partners:partner_images')


@login_required
@user_passes_test(is_partner)
def delete_partner_image(request, image_id):
    """Delete partner image"""
    partner = request.user.partner_profile
    image = get_object_or_404(PartnerImage, id=image_id, partner=partner)
    
    # Delete the actual file if it exists
    if image.image:
        if default_storage.exists(image.image.path):
            default_storage.delete(image.image.path)
    
    image.delete()
    messages.success(request, 'Image deleted successfully.')
    return redirect('partners:partner_images')


@login_required
@user_passes_test(is_partner)
def set_primary_image(request, image_id):
    """Set an image as primary for its type"""
    partner = request.user.partner_profile
    image = get_object_or_404(PartnerImage, id=image_id, partner=partner)
    
    # Unset other primary images of same type
    PartnerImage.objects.filter(
        partner=partner, 
        image_type=image.image_type, 
        is_primary=True
    ).update(is_primary=False)
    
    # Set this image as primary
    image.is_primary = True
    image.save()
    
    messages.success(request, f'{image.get_image_type_display()} set as primary successfully!')
    return redirect('partners:partner_images')


@login_required
@user_passes_test(is_partner)
def reorder_images(request):
    """Reorder partner images"""
    if request.method == 'POST':
        partner = request.user.partner_profile
        order_data = json.loads(request.POST.get('order', '[]'))
        
        for item in order_data:
            image_id = item.get('id')
            order = item.get('order')
            PartnerImage.objects.filter(id=image_id, partner=partner).update(display_order=order)
        
        return JsonResponse({'success': True})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)