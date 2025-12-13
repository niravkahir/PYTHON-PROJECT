from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Watchlist, Person
from django.contrib.auth.decorators import login_required
from django.urls import reverse

def home(request):
    movies = Movie.objects.all()
    
    # Search
    search = request.GET.get("search")
    if search:
        movies = movies.filter(title__icontains=search)

    # Sort
    sort = request.GET.get("sort")
    if sort == "name":
        movies = movies.order_by("title")
    elif sort == "rating":
        movies = movies.order_by("-rating")

    return render(request, "movie_and_webseries_reccomandation.app/home.html", {"movies": movies})

def add_movie(request):
    if request.method == "POST":
        title = request.POST["title"]
        genre = request.POST["genre"]
        rating = request.POST["rating"]
        poster = request.POST["poster"]

        Movie.objects.create(
            title=title,
            genre=genre,
            rating=rating,
            poster_url=poster
        )
        return redirect("movie_and_webseries_reccomandation.app:home")
    
    return render(request, "movie_and_webseries_reccomandation.app/add_movie.html")

def delete_movie(request, id):
    movie = get_object_or_404(Movie, id=id)
    movie.delete()
    return redirect("movie_and_webseries_reccomandation.app:home")

def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    is_in_watchlist = False
    if request.user.is_authenticated:
        is_in_watchlist = Watchlist.objects.filter(user=request.user, movie=movie).exists()
    return render(request, "movie_and_webseries_reccomandation.app/movie_detail.html", {
        "movie": movie,
        "is_in_watchlist": is_in_watchlist,
    })

@login_required
def watchlist_toggle(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    wl, created = Watchlist.objects.get_or_create(user=request.user, movie=movie)
    if not created:
        wl.delete()
    return redirect(reverse("movie_and_webseries_reccomandation.app:movie_detail", args=[pk]))

@login_required
def my_watchlist(request):
    items = Watchlist.objects.filter(user=request.user).select_related("movie").order_by("-added_at")
    movies = [item.movie for item in items]
    return render(request, "movie_and_webseries_reccomandation.app/my_watchlist.html", {"movies": movies})
