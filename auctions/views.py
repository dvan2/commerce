from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils import timezone

from .models import User, Listing, Bidding


def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        'heading': "Active Listing",
        'listings' : listings})

@login_required
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
            start_price =bid,
            owner= request.user,
            url=url,
            category=category,
            current_bid = bid
        )

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

    if request.user.is_authenticated:
        listing.watched = request.user.watchlist.filter(id=listing_id).exists()
        listing.is_owner = (listing.owner == request.user)
        current_bid = Bidding.objects.filter(listing=listing).order_by('-amount').first()

        if current_bid:
            listing.winning_user = current_bid.bidder == request.user
        else:
            listing.winner_user = False
        
        bidding_history = listing.bids.order_by('-amount')
        if request.method == "POST":
            try:
                new_bid = float(request.POST.get("new-bid"))
            except ValueError:
                messages.error(request, "Bid value must be a number")
                return render(request, "auctions/listing.html", {"listing": listing})
            old_bid = listing.current_bid
            if new_bid < 0:
                messages.error(request, "Bid value must be postive")
            elif new_bid <= old_bid:
                messages.error(request, "Bid value must be greater than previous bid.")
            else:
                new_bidding =  Bidding(
                    bidder=request.user,
                    listing=listing,
                    amount=new_bid
                )

                new_bidding.save()
                listing.current_bid = new_bid
                listing.save()
                messages.success(request, "Your bid was successful")
            return redirect('listing', listing_id=listing_id)

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "bidding_history" : bidding_history
    })

@login_required
def watch_list(request, listing_id=None):
    user = request.user
    if request.method == "POST" and listing_id is not None:
        try:
            listing = Listing.objects.get(id=listing_id)
        except Listing.DoesNotExist:
            return HttpResponseBadRequest("Listing not found.")
        
        watched = False
        if listing in user.watchlist.all():
            user.watchlist.remove(listing)
            watched= False
        else:
            user.watchlist.add(listing)
            watched = True

        listing.watched = watched
        return redirect('listing', listing_id = listing_id)
    else:
        return render(request, "auctions/index.html", {
            "heading": "Watch List",
            "listings": user.watchlist.all()
        })

@login_required
def close(request, listing_id):
    try:
        listing = Listing.objects.get(id=listing_id)
    except Listing.DoesNotExist:
        return HttpResponseBadRequest("Listing not found.")
    if request.method == "POST" and listing_id is not None:
        # get winner
        winner = Bidding.objects.filter(listing=listing).order_by('-amount').first()
        if not winner:
            return HttpResponseBadRequest("No bids found for this listing.")
        
        listing.winner = winner.bidder
        listing.closed_date = timezone.now()
        
        return redirect('index')
    
    return redirect('index')
 
@login_required
def profile(request):
    return render(request, 'auctions/profile.html')

@login_required
def winnings(request):
    user = request.user
    winning_bids = user.winner_listing.all()
    return render(request, 'auctions/winnings.html', 
                  { 'heading': "Your winning items", 
                  'listings': winning_bids})
            
@login_required
def active_bids(request):
    user = request.user
    active_listings= Listing.objects.filter(bids__bidder=user).distinct()
    return render(request, 'auctions/index.html', 
                  { 'heading': "Active Bids", 
                  'listings': active_listings})
            
@login_required
def user_listings(request):
    user = request.user
    owner_listings = user.listings.all()
    return render(request, 'auctions/index.html', 
                  { 'heading': "Your Listings", 
                  'listings': owner_listings})
            