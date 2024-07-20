from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    watchlist = models.ManyToManyField('Listing', related_name="watched_by")

class Listing(models.Model):
    class Category(models.TextChoices):
        OTHER = 'OTH', 'Other'
        ELECTRONICS = 'ELEC', 'Electronics'
        FASHION = 'FASH', 'Fashion'
        HOME = 'HOME', 'Home'
        BOOKS = 'BOOK', 'Books'
        TOYS = 'TOYS', 'Toys'

    title= models.CharField(max_length=100)
    description= models.TextField()
    start_price = models.DecimalField(max_digits=10, decimal_places=2)
    url = models.URLField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    category = models.CharField(max_length=5, choices=Category.choices, default=Category.OTHER)
    date = models.DateTimeField(auto_now_add=True)

    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='winner_listing', null=True, blank=True, default=None)
    current_bid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    closed_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.category}) - {self.owner.username}"


# class ClosedListing(models.Model):
#     class Category(models.TextChoices):
#         OTHER = 'OTH', 'Other'
#         ELECTRONICS = 'ELEC', 'Electronics'
#         FASHION = 'FASH', 'Fashion'
#         HOME = 'HOME', 'Home'
#         BOOKS = 'BOOK', 'Books'
#         TOYS = 'TOYS', 'Toys'

#     title = models.CharField(max_length=100)
#     description = models.TextField()
#     bid = models.DecimalField(max_digits=10, decimal_places=2)
#     url = models.URLField(max_length=200)
#     owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='closed_listings')
#     category = models.CharField(max_length=5, choices=Category.choices, default=Category.OTHER)
#     date = models.DateTimeField(auto_now_add=True)
#     closed_date = models.DateTimeField(auto_now_add=True)
#     winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='winner_listing')

class Bidding(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, related_name='bids', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    bid_date = models.DateTimeField(auto_now_add=True)