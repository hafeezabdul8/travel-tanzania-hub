from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import datetime, timedelta
from hotels.models import Booking, Hotel
from tourism.models import TourPackage, TourBooking
from .models import PlatformEarning
from partners.models import Partner

def is_admin(user):
    """Check if user is admin"""
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    """Main admin dashboard"""
    
    # Time periods
    today = datetime.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    # Hotel Statistics
    hotel_stats = {
        'total_bookings': Booking.objects.count(),
        'confirmed_bookings': Booking.objects.filter(status='confirmed').count(),
        'today_bookings': Booking.objects.filter(created_at__date=today).count(),
        'weekly_bookings': Booking.objects.filter(created_at__gte=week_ago).count(),
        'monthly_bookings': Booking.objects.filter(created_at__gte=month_ago).count(),
    }
    
    # Financial Statistics
    total_hotel_commission = Booking.objects.aggregate(
        Sum('platform_commission')
    )['platform_commission__sum'] or 0
    
    financial_stats = {
        'total_revenue': total_hotel_commission,
        'today_revenue': Booking.objects.filter(
            created_at__date=today
        ).aggregate(Sum('platform_commission'))['platform_commission__sum'] or 0,
        'weekly_revenue': Booking.objects.filter(
            created_at__gte=week_ago
        ).aggregate(Sum('platform_commission'))['platform_commission__sum'] or 0,
        'monthly_revenue': Booking.objects.filter(
            created_at__gte=month_ago
        ).aggregate(Sum('platform_commission'))['platform_commission__sum'] or 0,
    }
    
    # Top Hotels by Commission
    top_hotels = Booking.objects.values(
        'hotel__name', 'hotel__city'
    ).annotate(
        total_bookings=Count('id'),
        total_commission=Sum('platform_commission')
    ).order_by('-total_commission')[:10]
    
    # Recent Bookings
    recent_bookings = Booking.objects.select_related(
        'user', 'hotel'
    ).order_by('-created_at')[:10]
    
    # City-wise Distribution
    city_stats = Booking.objects.values(
        'hotel__city'
    ).annotate(
        bookings=Count('id'),
        revenue=Sum('platform_commission')
    )
    
    context = {
        'hotel_stats': hotel_stats,
        'financial_stats': financial_stats,
        'top_hotels': top_hotels,
        'recent_bookings': recent_bookings,
        'city_stats': city_stats,
        'today': today,
    }
    
    return render(request, 'dashboard/admin_dashboard.html', context)

@login_required
@user_passes_test(is_admin)
def partner_management(request):
    """Admin view for managing partners"""
    
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
    
    return render(request, 'dashboard/partner_management.html', context)


@login_required
def financial_reports(request):
    if not request.user.is_staff and not request.user.is_superuser:
        return redirect('home')
    
    # Default date range: last 30 days
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=30)
    
    # Get filter parameters
    report_type = request.GET.get('report_type', 'all')
    start_date_param = request.GET.get('start_date')
    end_date_param = request.GET.get('end_date')
    
    if start_date_param:
        start_date = datetime.strptime(start_date_param, '%Y-%m-%d').date()
    if end_date_param:
        end_date = datetime.strptime(end_date_param, '%Y-%m-%d').date()
    
    # Get bookings in date range
    bookings = Booking.objects.filter(
        created_at__date__range=[start_date, end_date],
        status='confirmed'
    )
    
    # Summary statistics
    total_commission = bookings.aggregate(total=Sum('platform_commission'))['total'] or 0
    total_bookings = bookings.count()
    avg_commission = total_commission / total_bookings if total_bookings > 0 else 0
    
    # Hotel statistics
    hotels_with_stats = []
    hotels = Hotel.objects.all()
    for hotel in hotels:
        hotel_bookings = bookings.filter(hotel=hotel)
        hotel_total = hotel_bookings.aggregate(total=Sum('total_price'))['total'] or 0
        hotel_commission = hotel_bookings.aggregate(total=Sum('platform_commission'))['total'] or 0
        hotel_bookings_count = hotel_bookings.count()
        
        if hotel_bookings_count > 0:
            hotels_with_stats.append({
                'name': hotel.name,
                'city': hotel.city,
                'get_city_display': hotel.get_city_display(),
                'total_revenue': hotel_total,
                'total_commission': hotel_commission,
                'total_bookings': hotel_bookings_count,
            })
    
    # Sort hotels by commission (descending)
    hotels_with_stats.sort(key=lambda x: x['total_commission'], reverse=True)
    
    # City statistics
    city_stats = bookings.values('hotel__city').annotate(
        revenue=Sum('total_price'),
        commission=Sum('platform_commission'),
        bookings=Count('id')
    ).order_by('-revenue')
    
    # Monthly trends (last 6 months)
    monthly_trends = []
    for i in range(6):
        month_date = end_date - timedelta(days=30*i)
        month_start = month_date.replace(day=1)
        if i < 5:
            next_month = month_start + timedelta(days=32)
            month_end = next_month.replace(day=1) - timedelta(days=1)
        else:
            month_end = end_date
        
        month_bookings = Booking.objects.filter(
            created_at__date__range=[month_start, month_end],
            status='confirmed'
        )
        
        month_commission = month_bookings.aggregate(total=Sum('platform_commission'))['total'] or 0
        month_revenue = month_bookings.aggregate(total=Sum('total_price'))['total'] or 0
        month_count = month_bookings.count()
        
        monthly_trends.append({
            'month': month_start,
            'commission': month_commission,
            'revenue': month_revenue,
            'bookings': month_count,
            'growth': 0  # You can calculate growth from previous month
        })
    
    context = {
        'start_date': start_date,
        'end_date': end_date,
        'report_type': report_type,
        'summary': {
            'total_commission': total_commission,
            'total_bookings': total_bookings,
            'avg_commission': avg_commission,
            'hotel_count': len(hotels_with_stats),
        },
        'hotels_with_stats': hotels_with_stats[:10],  # Top 10 hotels
        'city_stats': city_stats,
        'monthly_trends': monthly_trends,
        'detailed_transactions': bookings.order_by('-created_at')[:50],  # Last 50 transactions
        'top_city': city_stats.first() if city_stats else None,
        'commission_rate': 15,  # Your platform commission rate (15% as example)
    }
    
    return render(request, 'dashboard/financial_reports.html', context)


# ADD THIS VIEW TOO:
@login_required
@user_passes_test(is_admin)
def booking_management(request):
    """Admin view for managing all bookings"""
    
    bookings = Booking.objects.all().select_related('user', 'hotel').order_by('-created_at')
    
    # Filter by status if provided
    status_filter = request.GET.get('status', '')
    if status_filter:
        bookings = bookings.filter(status=status_filter)
    
    context = {
        'bookings': bookings,
        'status_filter': status_filter,
    }
    
    return render(request, 'dashboard/booking_management.html', context)
