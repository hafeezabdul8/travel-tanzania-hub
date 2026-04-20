import csv
from pathlib import Path
from pyexpat.errors import messages

from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum, Count, Q
from django.utils import timezone
from django.core.paginator import Paginator
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



@login_required
@user_passes_test(is_admin)
def add_training_example(request):
    """Add a new training example to the chatbot CSV file"""
    
    if request.method == 'POST':
        text = request.POST.get('text', '').strip()
        intent = request.POST.get('intent', '').strip()
        response = request.POST.get('response', '').strip()
        category = request.POST.get('category', 'general')
        keywords = request.POST.get('keywords', '')
        
        if not text or not intent or not response:
            # Use a simple error message without messages framework
            context = {
                'error': 'Please fill in all required fields',
                'training_stats': get_training_stats(),
                'intents': [...],  # Your intents list
                'categories': [...],  # Your categories list
            }
            return render(request, 'chatbot/add_training.html', context)
        
        # Path to CSV file
        csv_path = Path('chatbot/data/training_data.csv')
        csv_path.parent.mkdir(exist_ok=True, parents=True)
        
        file_exists = csv_path.exists()
        
        # Append to CSV
        with open(csv_path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(['text', 'intent', 'response', 'category', 'keywords'])
            writer.writerow([text, intent, response, category, keywords])
        
        # Success message
        context = {
            'success': f'✅ Training example added successfully! The chatbot will now respond to "{text[:50]}..."',
            'training_stats': get_training_stats(),
            'intents': [
                {'value': 'greeting', 'label': '👋 Greeting', 'color': 'blue'},
                {'value': 'hotel_booking', 'label': '🏨 Hotel Booking', 'color': 'green'},
                {'value': 'tourism', 'label': '🦁 Tourism', 'color': 'yellow'},
                {'value': 'afcon', 'label': '⚽ AFCON', 'color': 'pink'},
                {'value': 'price_query', 'label': '💰 Price Query', 'color': 'indigo'},
                {'value': 'transport', 'label': '🚗 Transport', 'color': 'orange'},
                {'value': 'food', 'label': '🍲 Food', 'color': 'emerald'},
                {'value': 'emergency', 'label': '🚨 Emergency', 'color': 'red'},
                {'value': 'farewell', 'label': '👋 Farewell', 'color': 'gray'},
                {'value': 'general', 'label': '📝 General', 'color': 'purple'},
            ],
            'categories': [
                'general', 'booking', 'tourism', 'afcon', 'pricing', 'transport', 'food', 'emergency'
            ]
        }
        
        return render(request, 'chatbot/add_training.html', context)
    
    # GET request - show the form
    context = {
        'training_stats': get_training_stats(),
        'intents': [
            {'value': 'greeting', 'label': '👋 Greeting', 'color': 'blue'},
            {'value': 'hotel_booking', 'label': '🏨 Hotel Booking', 'color': 'green'},
            {'value': 'tourism', 'label': '🦁 Tourism', 'color': 'yellow'},
            {'value': 'afcon', 'label': '⚽ AFCON', 'color': 'pink'},
            {'value': 'price_query', 'label': '💰 Price Query', 'color': 'indigo'},
            {'value': 'transport', 'label': '🚗 Transport', 'color': 'orange'},
            {'value': 'food', 'label': '🍲 Food', 'color': 'emerald'},
            {'value': 'emergency', 'label': '🚨 Emergency', 'color': 'red'},
            {'value': 'farewell', 'label': '👋 Farewell', 'color': 'gray'},
            {'value': 'general', 'label': '📝 General', 'color': 'purple'},
        ],
        'categories': [
            'general', 'booking', 'tourism', 'afcon', 'pricing', 'transport', 'food', 'emergency'
        ]
    }
    
    return render(request, 'chatbot/add_training.html', context)
def get_training_stats():
    """Get statistics about training data"""
    csv_path = Path('chatbot/data/training_data.csv')
    
    if not csv_path.exists():
        return {
            'total_examples': 0,
            'intents_count': 0,
            'last_updated': None,
            'intents_distribution': {},
        }
    
    try:
        import pandas as pd
        df = pd.read_csv(csv_path)
        
        stats = {
            'total_examples': len(df),
            'intents_count': df['intent'].nunique() if 'intent' in df.columns else 0,
            'last_updated': datetime.fromtimestamp(csv_path.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
            'intents_distribution': df['intent'].value_counts().to_dict() if 'intent' in df.columns else {},
        }
        return stats
    except:
        return {
            'total_examples': 0,
            'intents_count': 0,
            'last_updated': None,
            'intents_distribution': {},
        }

@login_required
@user_passes_test(is_admin)
def training_stats_view(request):
    """AJAX endpoint to get training statistics"""
    stats = get_training_stats()
    return JsonResponse(stats)

@login_required
@user_passes_test(is_admin)
def bulk_import_training(request):
    """Bulk import training examples from a CSV file"""
    
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        
        # Validate file type
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a CSV file')
            return redirect('dashboard:add_training_example')
        
        # Path to save uploaded file
        upload_path = Path('chatbot/data/uploaded_training.csv')
        upload_path.parent.mkdir(exist_ok=True, parents=True)
        
        # Save uploaded file
        with open(upload_path, 'wb+') as destination:
            for chunk in csv_file.chunks():
                destination.write(chunk)
        
        # Merge with existing training data
        main_csv_path = Path('chatbot/data/training_data.csv')
        
        try:
            import pandas as pd
            existing_df = pd.read_csv(main_csv_path) if main_csv_path.exists() else pd.DataFrame()
            new_df = pd.read_csv(upload_path)
            
            # Combine dataframes
            combined_df = pd.concat([existing_df, new_df], ignore_index=True)
            combined_df.drop_duplicates(subset=['text'], keep='first', inplace=True)
            
            # Save merged data
            combined_df.to_csv(main_csv_path, index=False)
            
            messages.success(request, f'✅ Successfully imported {len(new_df)} new training examples! Total examples: {len(combined_df)}')
            
            # Clean up uploaded file
            upload_path.unlink()
            
        except Exception as e:
            messages.error(request, f'Error processing CSV: {str(e)}')
        
        return redirect('dashboard:add_training_example')
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@login_required
@user_passes_test(is_admin)
def export_training_data(request):
    """Export all training data as CSV"""
    
    csv_path = Path('chatbot/data/training_data.csv')
    
    if not csv_path.exists():
        messages.error(request, 'No training data found')
        return redirect('dashboard:add_training_example')
    
    import csv
    from django.http import HttpResponse
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="chatbot_training_data.csv"'
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        writer = csv.writer(response)
        reader = csv.reader(f)
        for row in reader:
            writer.writerow(row)
    
    return response

def get_training_stats():
    """Get statistics about training data"""
    csv_path = Path('chatbot/data/training_data.csv')
    
    if not csv_path.exists():
        return {
            'total_examples': 0,
            'intents_count': 0,
            'last_updated': None,
            'intents_distribution': {},
        }
    
    try:
        import pandas as pd
        df = pd.read_csv(csv_path)
        
        stats = {
            'total_examples': len(df),
            'intents_count': df['intent'].nunique() if 'intent' in df.columns else 0,
            'last_updated': datetime.fromtimestamp(csv_path.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
            'intents_distribution': df['intent'].value_counts().to_dict() if 'intent' in df.columns else {},
        }
        return stats
    except:
        return {
            'total_examples': 0,
            'intents_count': 0,
            'last_updated': None,
            'intents_distribution': {},
        }

