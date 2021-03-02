from django.contrib import admin
from .models import Comment, Listing

# Register your models here.


class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "current_price", "image_url", "date_created", "active")


class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "listing_id", "user_id", "comment", "cm_time")


admin.site.register(Listing, ListingAdmin)
admin.site.register(Comment, CommentAdmin)


