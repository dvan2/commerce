from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

from .models import User, Listing


def index(request):
    listings = Listing.objects.all()
    print(listings)
    return render(request, "auctions/index.html", {'listings' : listings})

def create(request):
    categories = Listing.Category.choices
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        bid = request.POST.get("bid")
        url = request.POST.get("url")
        category = request.POST.get("category")

        if category not in dict(Listing.Category.choices):
            messages.error(request, "Invalid category.")
            return render(request, "auctions/create.html")
        
        # Empty input
        if not title or not description or not bid:
            messages.error(request, "Please complete all fields.")
            return render(request, "auctions/create.html")
        
        try:
            bid = int(bid)
        except ValueError:
            messages.error(request, "Starting bid must be a number.")
            return render(request, "auctions/create.html")
        
        if bid <0:
            messages.error(request,"Starting bid cannot be negative.")
            return render(request, "auctions/create.html")
        
        # Process the listing to db
        listing = Listing.objects.create(
            title=title,
            description= description,
            bid=bid,
            url=url,
            category=category
        )

        print("Title:", listing.title)
    print(categories)
    return render(request, "auctions/create.html", {'categories': categories})

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def listing(request, listing_id):
    try:
        listing = Listing.objects.get(id=listing_id)
    except Listing.DoesNotExist:
        return HttpResponseBadRequest("Listing not found.")
    return render(request, "auctions/listing.html", {
        "listing": listing
    })