from django.shortcuts import render, redirect
from commerce import svm_toxic_comment
from .models import Listing, Comment


def index(request, **kwargs):

    my_array = svm_toxic_comment.train()

    try:
        user_id = request.session["user_id"]
    except Exception:
        user_watchlist = []

    return render(request, "auctions/index.html", {
        "Listings": Listing.objects.filter(active=True),
        "user_watchlist": user_watchlist,
        "my_array": my_array
    })


def listing_page(request, listing_id, **kwargs):
    who_is_here = "Somebody"

    if not request.session.is_empty():
        user_id = request.session["user_id"]

        try:
            user_id = request.session["user_id"]
        except Exception:
            user_watchlist = []

    # check for the comments
    try:
        comments = Comment.objects.filter(listing_id=listing_id)
    except Comment.DoesNotExist:
        comments = []

    return render(request, "auctions/listing_page.html", {
        "listing": Listing.objects.get(pk=listing_id),
        "who_is_here": who_is_here,
        "comments": comments,
    })


def add_comment(request, listing_id):
    user_id = request.session["user_id"]

    # if comment is empty, send the error message
    comment = request.POST["comment"]
    if not comment:
        return redirect(f"/listing/{listing_id}")

    comment = Comment.objects.create(
        listing_id=listing_id,
        comment=comment
    )

    return redirect(f"/listing/{listing_id}")
