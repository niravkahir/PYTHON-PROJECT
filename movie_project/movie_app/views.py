from django.shortcuts import render, redirect
from .models import Movie

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

    return render(request, "home.html", {"movies": movies})


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
        return redirect("/")
    
    return render(request, "add_movie.html")

def delete_movie(request, id):
    movie = Movie.objects.get(id=id)
    movie.delete()
    return redirect("/")
