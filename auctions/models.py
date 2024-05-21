from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    class Category(models.TextChoices):
        ELECTRONICS = 'ELEC', 'Electronics'
        FASHION = 'FASH', 'Fashion'
        HOME = 'HOME', 'Home'
        BOOKS = 'BOOK', 'Books'
        TOYS = 'TOYS', 'Toys'
        OTHER = 'OTH', 'Other'

    title= models.CharField(max_length=100)
    description= models.TextField()
    bid = models.DecimalField(max_digits=10, decimal_places=2)
    url = models.URLField(max_length=200)
    category = models.CharField(max_length=5, choices=Category.choices, default=Category.OTHER)
