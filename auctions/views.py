from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Bid, User, AuctionListing, Comment


def index(request):
    # Retrieve all listings
    listings = AuctionListing.objects.all()

    # Retrieve the highest bid for each listing
    for listing in listings:
        listing.highest_bid = Bid.objects.filter(listing=listing).order_by('-amount').first()

    return render(request, 'auctions/index.html', {
        'listings': listings
    })


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


@login_required
def create_listing(request):
    if request.method == 'POST':
        # Retrieve listing data from the form submission
        title = request.POST['title']
        description = request.POST['description']
        starting_price = request.POST['starting_price']
        image_url = request.POST.get('image_url', '')
        category = request.POST['category']
        created_by = request.user  # Set the created_by field to the logged-in user

        # Create a new AuctionListing instance
        listing = AuctionListing(
            title=title,
            description=description,
            starting_price=starting_price,
            image_url=image_url,
            category=category,
            created_by=created_by
        )
        listing.save()

        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'auctions/create_listing.html')


def listing(request, listing_id):
    try:
        listing = AuctionListing.objects.get(pk=listing_id)
    except AuctionListing.DoesNotExist:
        return render(request, "auctions/index.html", {
            "message": "Listing does not exist."
        })

    # Retrieve the message from the query parameters
    message = request.GET.get("message", "")

    return render(request, 'auctions/listing.html', {
        'listing': listing,
        'comments': listing.comments.all(),
        'watchers': listing.watchers.all(),
        'highest_bid': listing.bid.all().order_by('-amount').first(),
        'message': message
    })


@login_required
def watchlist(request):
    watchlist = request.user.watchlist.all()
    return render(request, 'auctions/watchlist.html', {
        'watchlist': watchlist
    })


@login_required
def add_watchlist(request, listing_id):
    listing = AuctionListing.objects.get(pk=listing_id)
    listing.watchers.add(request.user)
    return HttpResponseRedirect(reverse('listing', kwargs={'listing_id': listing_id}))


@login_required
def remove_watchlist(request, listing_id):
    listing = AuctionListing.objects.get(pk=listing_id)
    listing.watchers.remove(request.user)
    return HttpResponseRedirect(reverse('listing', kwargs={'listing_id': listing_id}))


@login_required
def close_auction(request, listing_id):
    listing = AuctionListing.objects.get(pk=listing_id, created_by=request.user)

    # Check if the auction is already closed
    if listing.closed:
        return HttpResponseRedirect(reverse('listing', listing_id=listing_id))

    # Close the auction
    listing.closed = True

    # Determine the highest bidder and set them as the winner
    highest_bid = Bid.objects.filter(listing=listing).order_by('-amount').first()
    if highest_bid:
        listing.winner = highest_bid.user

    # Save the changes
    listing.save()

    return HttpResponseRedirect(reverse('listing', kwargs={'listing_id': listing_id}))


@login_required
def place_bid(request, listing_id):
    # Get the bid amount from the form submission
    bid_amount = request.POST.get('bid_amount')

    # Validate bid amount
    if bid_amount is None:
        return HttpResponseRedirect(reverse('listing', args=[listing_id]) + "?message=Please enter a valid bid amount.")

    try:
        bid_amount = float(bid_amount)
    except ValueError:
        return HttpResponseRedirect(reverse('listing', args=[listing_id]) + "?message=Please enter a valid bid amount.")

    # Check bid amount against listing conditions
    listing = AuctionListing.objects.get(pk=listing_id)
    if bid_amount <= listing.starting_price:
        return HttpResponseRedirect(reverse('listing', args=[listing_id]) + "?message=Bid amount must be higher than the starting bid.")

    highest_bid = Bid.objects.filter(listing=listing).order_by('-amount').first()
    if highest_bid and bid_amount <= highest_bid.amount:
        return HttpResponseRedirect(reverse('listing', args=[listing_id]) + "?message=Bid amount must be higher than the current highest bid.")

    # Place the bid
    Bid.objects.create(listing=listing, user=request.user, amount=bid_amount)

    return HttpResponseRedirect(reverse('listing', args=[listing_id]) + "?message=Bid placed successfully!")


@login_required
def add_comment(request, listing_id):
    listing = AuctionListing.objects.get(pk=listing_id)
    if request.method == 'POST':
        text = request.POST['text']
        comment = Comment(listing=listing, user=request.user, text=text)
        comment.save()
    return HttpResponseRedirect(reverse('listing', args=[listing_id]))


def categories(request):
    # Retrieve the list of categories with the count of listings in each category
    categories = AuctionListing.objects.values('category').annotate(total=Count('category')).order_by('category')
    return render(request, 'auctions/categories.html', {'categories': categories})


def category_listings(request, category):
    # Retrieve the listings in the specified category
    listings = AuctionListing.objects.filter(category=category)
    return render(request, 'auctions/category_listings.html', {'category': category, 'listings': listings})
