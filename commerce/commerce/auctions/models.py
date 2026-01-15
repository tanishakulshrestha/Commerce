from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name
class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(blank=True)
    category = models.CharField(max_length=64, blank=True)

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="owned_listings"   # ✅ CHANGE HERE
    
    )
    active = models.BooleanField(default=True) 
    winner = models.ForeignKey(
    User,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name="won_auctions"
)
    watchlist = models.ManyToManyField(
        User,
        blank=True,
        related_name="watchlisted_items"
    )
class Comment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} on {self.listing}"

    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Bid(models.Model):
    bidder = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="bids"              # ✅ DIFFERENT NAME
    )

    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name="bids"
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class ListingImage(models.Model):
    listing = models.ForeignKey(
        Listing,
        related_name="images",
        on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="listing_images/")
