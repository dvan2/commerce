from django.contrib import admin

from .models import Listing, Bidding

class ListingAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "owner")

# Register your models here.
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bidding)
