from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .models import User, Listing, Bid, Comment
from django.contrib import messages
from decimal import Decimal
from auctions.ml.predict import predict_price

<<<<<<< HEAD

=======
from .ml.predict import predict_price
from django.apps import apps
import pandas as pd
from django.contrib.auth.decorators import login_required
from django.contrib import messages
>>>>>>> afa1184cf0f46363e7f76887524811c32dccc145

# -----------------------------
# INDEX / ACTIVE LISTINGS
# -----------------------------
def index(request):
    listings = Listing.objects.filter(active=True)
    return render(request, "auctions/index.html", {
        "listings": listings
    })


# -----------------------------
# AUTHENTICATION
# -----------------------------
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })

        login(request, user)
        return HttpResponseRedirect(reverse("index"))

    return render(request, "auctions/register.html")


# -----------------------------
# CREATE LISTING (FIXED)
# -----------------------------
@login_required
def create(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["starting_bid"]
        image_url = request.POST.get("image_url")

        Listing.objects.create(
            title=title,
            description=description,
            starting_bid=starting_bid,
            image_url=image_url,
            owner=request.user
        )

        return redirect("index")

    return render(request, "auctions/create.html")

def listing(request, listing_id):
    from auctions.ml.predict import predict_price   # 👈 IMPORT HERE

    listing = get_object_or_404(Listing, pk=listing_id)

    predicted_price = predict_price(
        listing.category,
        len(listing.title),
        len(listing.description),
        1  # or your image count logic
    )

    ...


# -----------------------------
# LISTING DETAIL PAGE
# -----------------------------
def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)

<<<<<<< HEAD
=======
    predicted_price = predict_price(listing)

>>>>>>> afa1184cf0f46363e7f76887524811c32dccc145
    bids = listing.bids.all()
    highest_bid = bids.order_by("-amount").first()
    current_price = highest_bid.amount if highest_bid else listing.starting_bid
    comments = listing.comments.order_by("-created_at")
<<<<<<< HEAD
=======

>>>>>>> afa1184cf0f46363e7f76887524811c32dccc145
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "bids_count": bids.count(),
        "highest_bid": highest_bid,
        "current_price": current_price,
<<<<<<< HEAD
        "comments": comments

    })
=======
        "comments": comments,
        "predicted_price": predicted_price
    })

>>>>>>> afa1184cf0f46363e7f76887524811c32dccc145
@login_required
def watchlist(request):
    listings = request.user.watchlisted_items.all()
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })

@login_required
def toggle_watchlist(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)

    if request.user in listing.watchlist.all():
        listing.watchlist.remove(request.user)
        messages.info(request, "Removed from watchlist.")
    else:
        listing.watchlist.add(request.user)
        messages.success(request, "Added to watchlist.")

    return redirect("listing", listing_id=listing.id)

<<<<<<< HEAD

=======
def listing_detail(request, listing_id):
    listing = Listing.objects.get(id=listing_id)

    title_length = len(listing.title)
    description_length = len(listing.description)
    number_of_images = listing.images.count()

    predicted_price = predict_price(
        listing.category,
        title_length,
        description_length,
        number_of_images
    )

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "predicted_price": predicted_price
    })

@login_required
def create_listing(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["starting_bid"]
        category = request.POST["category"]
        image_url = request.POST.get("image_url")

        listing = Listing.objects.create(
            title=title,
            description=description,
            starting_bid=starting_bid,
            category=category,
            image_url=image_url,
            owner=request.user
        )

        messages.success(request, "Listing created successfully!")
        return redirect("listing", listing_id=listing.id)

    return render(request, "auctions/create_listing.html")
>>>>>>> afa1184cf0f46363e7f76887524811c32dccc145

# -----------------------------
# PLACE BID
# -----------------------------
@login_required
def place_bid(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)

    if not listing.active:
        messages.error(request, "This auction is closed.")
        return redirect("listing", listing_id=listing.id)

    if request.user == listing.owner:
        messages.error(request, "You cannot bid on your own listing.")
        return redirect("listing", listing_id=listing.id)

    bid_amount_str = request.POST.get("bid")
    if not bid_amount_str:
        messages.error(request, "Please enter a bid amount.")
        return redirect("listing", listing_id=listing.id)

    bid_amount = Decimal(bid_amount_str)

    highest_bid = listing.bids.order_by("-amount").first()
    current_price = highest_bid.amount if highest_bid else listing.starting_bid

    if bid_amount <= current_price:
        messages.error(request, "Your bid must be higher than the current price.")
        return redirect("listing", listing_id=listing.id)

    Bid.objects.create(
        listing=listing,
        bidder=request.user,
        amount=bid_amount
    )

    messages.success(request, "Bid placed successfully!")
    return redirect("listing", listing_id=listing.id)
@login_required
def close_auction(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)

    if request.user != listing.owner:
        messages.error(request, "Only the owner can close this auction.")
        return redirect("listing", listing_id=listing.id)

    listing.active = False
    listing.save()

    messages.success(request, "Auction closed successfully.")
    return redirect("listing", listing_id=listing.id)
@login_required
def toggle_watchlist(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)

    if request.user in listing.watchlist.all():
        listing.watchlist.remove(request.user)
        messages.info(request, "Removed from watchlist.")
    else:
        listing.watchlist.add(request.user)
        messages.success(request, "Added to watchlist.")

    return redirect("listing", listing_id=listing.id)
@login_required
<<<<<<< HEAD
=======

>>>>>>> afa1184cf0f46363e7f76887524811c32dccc145
def add_comment(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)

    text = request.POST.get("comment")
    if not text:
        messages.error(request, "Comment cannot be empty.")
        return redirect("listing", listing_id=listing.id)

    Comment.objects.create(
        user=request.user,
        listing=listing,
        text=text
    )

    return redirect("listing", listing_id=listing.id)
<<<<<<< HEAD
=======

def predict_price(listing):
    app_config = apps.get_app_config("auctions")
    model = app_config.model

    import pandas as pd

    data = pd.DataFrame([{
        "category": listing.category,
        "title_length": len(listing.title),
        "description_length": len(listing.description),
        "number_of_images": 1 if listing.image_url else 0
    }])

    predicted_price = model.predict(data)[0]
    return round(float(predicted_price), 2)
>>>>>>> afa1184cf0f46363e7f76887524811c32dccc145
