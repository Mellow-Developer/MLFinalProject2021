from django.contrib import admin
from .models import User, Bid, Comment, Category, Listing, Watchlist

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "cat")


class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "listing_id", "user_id", "bid", "active")


class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "long_title", "description", "starting_price", "current_price", "image_url", "cats",
                    "user", "date_created", "active")


class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username")


class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "listing_id", "user_id", "comment", "cm_time")


class WatchlistAdmin(admin.ModelAdmin):
    list_display = ("id", "listing_id", "user_id", "added")


admin.site.register(Listing, ListingAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Watchlist, WatchlistAdmin)

