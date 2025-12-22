from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q, Avg, Count
from .models import Movie, Watchlist, Review, UserProfile, ContentRequest
from django.contrib.auth.models import User
from django.contrib import messages

# Home page - redirects based on user
def home(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('movie_app:admin_home')
        else:
            return redirect('movie_app:user_home')
    else:
        return redirect('movie_app:user_home')

# User homepage
def user_home(request):
    movies = Movie.objects.all()
    
    # Search
    search = request.GET.get('search', '')
    if search:
        movies = movies.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search) |
            Q(genre__icontains=search) |
            Q(director__icontains=search)
        )
    
    # Filter by genre
    genre = request.GET.get('genre', '')
    if genre:
        movies = movies.filter(genre=genre)
    
    # Filter by rating
    rating = request.GET.get('rating', '')
    if rating:
        try:
            movies = movies.filter(rating__gte=float(rating))
        except:
            pass
    
    # Sort
    sort = request.GET.get('sort', '')
    if sort == 'title':
        movies = movies.order_by('title')
    elif sort == '-title':
        movies = movies.order_by('-title')
    elif sort == 'rating':
        movies = movies.order_by('rating')
    elif sort == '-rating':
        movies = movies.order_by('-rating')
    elif sort == '-release_year':
        movies = movies.order_by('-release_year')
    
    # Get genres for filter dropdown
    genres = Movie.objects.values_list('genre', flat=True).distinct()
    
    # Check if movie is in user's watchlist
    watchlist_movie_ids = []
    if request.user.is_authenticated:
        watchlist_movie_ids = Watchlist.objects.filter(
            user=request.user
        ).values_list('movie_id', flat=True)
    
    context = {
        'movies': movies,
        'genres': genres,
        'watchlist_movie_ids': watchlist_movie_ids,
    }
    return render(request, 'movie_app/user_home.html', context)

# Admin homepage (simple)
@staff_member_required
def admin_home(request):
    movies = Movie.objects.all()
    
    # Search
    search = request.GET.get('search', '')
    if search:
        movies = movies.filter(title__icontains=search)
    
    # Sort
    sort = request.GET.get('sort', '')
    if sort == 'name':
        movies = movies.order_by('title')
    elif sort == 'rating':
        movies = movies.order_by('-rating')
    
    context = {
        'movies': movies,
    }
    return render(request, 'movie_app/home.html', context)

# Admin dashboard (comprehensive)
@staff_member_required
def admin_dashboard(request):
    stats = {
        'total_users': User.objects.count(),
        'total_movies': Movie.objects.count(),
        'pending_requests': ContentRequest.objects.filter(status='pending').count(),
        'total_reviews': Review.objects.count(),
    }
    
    pending_requests = ContentRequest.objects.filter(status='pending').order_by('-created_at')[:5]
    recent_users = User.objects.order_by('-date_joined')[:5]
    
    context = {
        'stats': stats,
        'pending_requests': pending_requests,
        'recent_users': recent_users,
    }
    return render(request, 'movie_app/admin_dashboard.html', context)

# Login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('movie_app:home')
    else:
        form = AuthenticationForm()
    
    return render(request, 'movie_app/login.html', {'form': form})

# Register view
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create user profile
            UserProfile.objects.create(user=user)
            
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('movie_app:user_home')
    else:
        form = UserCreationForm()
    
    return render(request, 'movie_app/register.html', {'form': form})

# Logout view
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('movie_app:user_home')

# Movie detail view
def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    reviews = Review.objects.filter(movie=movie).order_by('-created_at')
    
    # Check if in watchlist
    is_in_watchlist = False
    if request.user.is_authenticated:
        is_in_watchlist = Watchlist.objects.filter(
            user=request.user, movie=movie
        ).exists()
    
    context = {
        'movie': movie,
        'reviews': reviews,
        'is_in_watchlist': is_in_watchlist,
    }
    return render(request, 'movie_app/movie_detail.html', context)

# Add movie (admin only)
@staff_member_required
def add_movie(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        genre = request.POST.get('genre')
        rating = request.POST.get('rating')
        description = request.POST.get('description', '')
        poster_url = request.POST.get('poster_url', '')
        
        movie = Movie.objects.create(
            title=title,
            genre=genre,
            rating=float(rating),
            description=description,
            poster_url=poster_url
        )
        messages.success(request, f'Movie "{title}" added successfully!')
        return redirect('movie_app:admin_home')
    
    return render(request, 'movie_app/add_movie.html')

# Delete movie (admin only)
@staff_member_required
def delete_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    movie.delete()
    messages.success(request, f'Movie "{movie.title}" deleted successfully!')
    return redirect('movie_app:admin_home')

# Watchlist views
@login_required
def watchlist(request):
    watchlist_items = Watchlist.objects.filter(user=request.user).select_related('movie')
    movies = [item.movie for item in watchlist_items]
    
    return render(request, 'movie_app/watchlist.html', {'movies': movies})

@login_required
def watchlist_toggle(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    
    # Check if already in watchlist
    watchlist_item = Watchlist.objects.filter(user=request.user, movie=movie).first()
    
    if watchlist_item:
        watchlist_item.delete()
        messages.info(request, f'Removed "{movie.title}" from watchlist')
    else:
        Watchlist.objects.create(user=request.user, movie=movie)
        messages.success(request, f'Added "{movie.title}" to watchlist')
    
    return redirect('movie_app:movie_detail', movie_id=movie_id)

# Review views
@login_required
def review_form(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        text = request.POST.get('text')
        
        # Update or create review
        review, created = Review.objects.update_or_create(
            movie=movie,
            user=request.user,
            defaults={
                'rating': int(rating),
                'text': text
            }
        )
        
        if created:
            messages.success(request, 'Review submitted!')
        else:
            messages.info(request, 'Review updated!')
        
        return redirect('movie_app:movie_detail', movie_id=movie_id)
    
    # Check if user already reviewed
    existing_review = Review.objects.filter(movie=movie, user=request.user).first()
    
    context = {
        'movie': movie,
        'existing_review': existing_review,
    }
    return render(request, 'movie_app/review_form.html', context)

# Profile view
def profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    reviews = Review.objects.filter(user=user).order_by('-created_at')[:5]
    watchlist_count = Watchlist.objects.filter(user=user).count()
    
    context = {
        'profile_user': user,
        'reviews': reviews,
        'watchlist_count': watchlist_count,
    }
    return render(request, 'movie_app/profile.html', context)

# Content request (for golden users)
@login_required
def content_request(request):
    if not request.user.profile.is_golden_user:
        messages.error(request, 'Only verified industry professionals can submit content requests.')
        return redirect('movie_app:user_home')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        genre = request.POST.get('genre')
        description = request.POST.get('description')
        request_type = request.POST.get('request_type', 'new')
        
        ContentRequest.objects.create(
            user=request.user,
            title=title,
            genre=genre,
            description=description,
            request_type=request_type
        )
        
        messages.success(request, 'Content request submitted for admin review!')
        return redirect('movie_app:user_home')
    
    return render(request, 'movie_app/content_request.html')

# Contact creator
def contact(request):
    if request.method == 'POST':
        # In a real app, you would save this to database or send email
        messages.success(request, 'Thank you for your message! We will get back to you soon.')
        return redirect('movie_app:user_home')
    
    return render(request, 'movie_app/contact.html')

# Search view
def search(request):
    query = request.GET.get('q', '')
    movies = Movie.objects.all()
    
    if query:
        movies = movies.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(genre__icontains=query) |
            Q(director__icontains=query)
        )
    
    context = {
        'movies': movies,
        'query': query,
    }
    return render(request, 'movie_app/search_results.html', context)