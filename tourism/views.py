
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Avg, Count
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import TouristAttraction, TourPackage, UserReview, AttractionImage, TourBooking

def tourism_view(request):
    # Get filters from request
    city = request.GET.get('city', '')
    category = request.GET.get('category', '')
    search = request.GET.get('search', '')
    
    # Start with all attractions and PREFETCH IMAGES
    attractions = TouristAttraction.objects.prefetch_related('images').all()
    
    # Apply filters
    if city:
        attractions = attractions.filter(city=city)
    
    if category:
        attractions = attractions.filter(category=category)
    
    if search:
        attractions = attractions.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search) |
            Q(location__icontains=search)
        )
    
    # Get counts for filters
    city_counts = TouristAttraction.objects.values('city').annotate(count=Count('id'))
    category_counts = TouristAttraction.objects.values('category').annotate(count=Count('id'))
    
    # Group attractions by city for display
    dar_attractions = attractions.filter(city='DAR')
    aru_attractions = attractions.filter(city='ARU')
    zan_attractions = attractions.filter(city='ZAN')
    all_attractions = attractions.filter(city='ALL')
    
    # Get featured tour packages
    featured_packages = TourPackage.objects.filter(is_featured=True)[:4]
    
    context = {
        'attractions': attractions,
        'dar_attractions': dar_attractions,
        'aru_attractions': aru_attractions,
        'zan_attractions': zan_attractions,
        'all_attractions': all_attractions,
        'featured_packages': featured_packages,
        'city_counts': city_counts,
        'category_counts': category_counts,
        'selected_city': city,
        'selected_category': category,
        'search_query': search,
    }
    return render(request, 'tourism/index.html', context)

def attraction_detail(request, attraction_id):
    # Use prefetch_related to get images efficiently
    attraction = get_object_or_404(
        TouristAttraction.objects.prefetch_related('images', 'tour_packages', 'reviews'), 
        id=attraction_id
    )
    tour_packages = attraction.tour_packages.all()
    reviews = attraction.reviews.all()
    related_attractions = TouristAttraction.objects.filter(city=attraction.city).exclude(id=attraction.id)[:4]
    
    # Calculate average rating
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    
    # Get primary image or first image
    primary_image = attraction.images.filter(is_primary=True).first()
    if not primary_image:
        primary_image = attraction.images.first()
    
    context = {
        'attraction': attraction,
        'tour_packages': tour_packages,
        'reviews': reviews,
        'related_attractions': related_attractions,
        'avg_rating': round(avg_rating, 1),
        'review_count': reviews.count(),
        'primary_image': primary_image,
        'all_images': attraction.images.all(),
    }
    return render(request, 'tourism/detail.html', context)

def tour_packages_view(request):
    packages = TourPackage.objects.select_related('attraction').prefetch_related('attraction__images')
    
    # Apply filters
    city = request.GET.get('city', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    
    if city:
        packages = packages.filter(attraction__city=city)
    
    if min_price:
        packages = packages.filter(price__gte=min_price)
    
    if max_price:
        packages = packages.filter(price__lte=max_price)
    
    context = {
        'packages': packages,
        'selected_city': city,
    }
    return render(request, 'tourism/packages.html', context)


@login_required
def book_tour_package(request, package_id):
    package = get_object_or_404(TourPackage, id=package_id)
    
    if request.method == 'POST':
        booking_date = request.POST.get('booking_date')
        number_of_people = int(request.POST.get('number_of_people', 1))
        special_requests = request.POST.get('special_requests', '')
        
        # Calculate total price
        total_price = package.price * number_of_people
        
        # Create booking
        booking = TourBooking.objects.create(
            user=request.user,
            tour_package=package,
            booking_date=booking_date,
            number_of_people=number_of_people,
            special_requests=special_requests,
            total_price=total_price,  # This should work now
            status='pending'
        )
        
        messages.success(request, f'Tour package "{package.name}" booked successfully! Total: ${total_price}')
        return redirect('tour_booking_confirmation', booking_id=booking.id)
    
    # Default booking date is tomorrow
    default_date = (timezone.now() + timezone.timedelta(days=1)).strftime('%Y-%m-%d')
    
    context = {
        'package': package,
        'default_date': default_date,
        'max_date': (timezone.now() + timezone.timedelta(days=90)).strftime('%Y-%m-%d'),
    }
    
    return render(request, 'tourism/book_package.html', context)
@login_required
def tour_booking_confirmation(request, booking_id):
    booking = get_object_or_404(TourBooking, id=booking_id, user=request.user)
    return render(request, 'tourism/booking_confirmation.html', {'booking': booking})

@login_required
def my_tour_bookings(request):
    bookings = TourBooking.objects.filter(user=request.user).order_by('-created_at')
    
    # Calculate counts for each status
    confirmed_count = bookings.filter(status='confirmed').count()
    pending_count = bookings.filter(status='pending').count()
    cancelled_count = bookings.filter(status='cancelled').count()
    completed_count = bookings.filter(status='completed').count()
    
    context = {
        'bookings': bookings,
        'confirmed_count': confirmed_count,
        'pending_count': pending_count,
        'cancelled_count': cancelled_count,
        'completed_count': completed_count,
        'total_count': bookings.count(),
    }
    return render(request, 'tourism/my_bookings.html', context)
@login_required
def cancel_tour_booking(request, booking_id):
    booking = get_object_or_404(TourBooking, id=booking_id, user=request.user)
    
    if booking.status == 'pending':
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, 'Tour booking cancelled successfully.')
    else:
        messages.error(request, 'Cannot cancel this booking. Please contact support.')
    
    return redirect('my_tour_bookings')

def package_quick_view(request, package_id):
    """API endpoint for package quick view modal"""
    try:
        package = TourPackage.objects.get(id=package_id)
        
        data = {
            'success': True,
            'package': {
                'id': package.id,
                'name': package.name,
                'description': package.description,
                'duration': package.duration,
                'price': str(package.price),
                'attraction': package.attraction.name,
                'city': package.attraction.get_city_display(),
                'includes': package.get_includes_list(),
                'excludes': package.get_excludes_list(),
            }
        }
        return JsonResponse(data)
    except TourPackage.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Package not found'})
    
    from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def add_review(request, attraction_id):
    attraction = get_object_or_404(TouristAttraction, id=attraction_id)
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment', '')
        
        # Check if user already reviewed
        existing_review = UserReview.objects.filter(
            user=request.user, 
            attraction=attraction
        ).first()
        
        if existing_review:
            existing_review.rating = rating
            existing_review.comment = comment
            existing_review.save()
            messages.success(request, 'Review updated successfully!')
        else:
            UserReview.objects.create(
                user=request.user,
                attraction=attraction,
                rating=rating,
                comment=comment
            )
            messages.success(request, 'Review submitted successfully!')
        
        return redirect('attraction_detail', attraction_id=attraction_id)
    
    return redirect('attraction_detail', attraction_id=attraction_id)
