from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from commerce import svm_toxic_comment
from .forms import NewListingForm
from .models import User, Listing, Category, Watchlist, Bid, Comment


def index(request, **kwargs):
    # check for user watchlist items

    my_array = svm_toxic_comment.train()

    try:
        user_id = request.session["user_id"]
        user_watchlist = Watchlist.objects.filter(user_id=user_id, added=True)
    except Exception:
        user_watchlist = []

    return render(request, "auctions/index.html", {
        "Listings": Listing.objects.filter(active=True),
        "user_watchlist": user_watchlist,
        "my_array": my_array
    })


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
            request.session['user_id'] = user.id
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required(login_url='login')
def new_listing(request):
    if request.method == "POST":
        title = request.POST["title"]
        long_title = request.POST["long_title"]
        description = request.POST["description"]
        starting_price = request.POST["starting_price"]
        image_url = request.POST["image_url"]
        cats = request.POST["cats"]
        user_id = request.session["user_id"]

        try:
            Listing.objects.create(
                title=title,
                long_title=long_title,
                description=description,
                starting_price=starting_price,

                image_url=image_url,
                cats=Category.objects.get(pk=cats),
                user=user_id
            )
            latest_listing = Listing.objects.latest('pk')
            latest_listing.current_price = Bid.objects.create(
                user_id=user_id,
                listing_id=latest_listing.pk,
                bid=starting_price
            )
            latest_listing.save()

            return redirect(reverse('index'))

        except ImportError:
            return render(request, "auctions/new_listing.html", {
                "status": "ImportError"
            })

    else:
        # check if the user is logged in
        if not request.session.is_empty():
            # check for user watchlist items
            try:
                user_id = request.session["user_id"]
                user_watchlist = Watchlist.objects.filter(user_id=user_id, added=True)
            except Exception:
                user_watchlist = []

            return render(request, "auctions/new_listing.html", {
                "form": NewListingForm(),
                "user_watchlist": user_watchlist
            })


def listing_page(request, listing_id, **kwargs):
    who_is_here = "Somebody"

    if not request.session.is_empty():
        user_id = request.session["user_id"]

        # check for user watchlist items
        try:
            user_id = request.session["user_id"]
            user_watchlist = Watchlist.objects.filter(user_id=user_id, added=True)
        except Exception:
            user_watchlist = []

        # this is a user check for a closed auction to declare who is watching this page
        bid_user = Bid.objects.get(listing_id=listing_id).user_id
        if bid_user == user_id:
            who_is_here = "The Winner"

    else:
        user_id = False
        user_watchlist = []
    watchlist_status = 0

    try:
        bid_status = kwargs['bid_status']
    except Exception:
        bid_status = 0

    # check for the comments
    try:
        comments = Comment.objects.filter(listing_id=listing_id)
    except Comment.DoesNotExist:
        comments = []

    # if the user is signed id then look for watchlist
    if user_id:
        try:
            watchlist_status = Watchlist.objects.get(user_id=user_id, listing_id=listing_id)
        except Watchlist.DoesNotExist:
            return render(request, "auctions/listing_page.html", {
                "listing": Listing.objects.get(pk=listing_id),
                "watchlist_status": 0,
                "sign_in": True,
                "bid_status": bid_status,
                "who_is_here": who_is_here,
                "comments": comments,
                "user_watchlist": user_watchlist
            })

    return render(request, "auctions/listing_page.html", {
        "listing": Listing.objects.get(pk=listing_id),
        "watchlist_status": watchlist_status,
        "sign_in": True,
        "bid_status": bid_status,
        "who_is_here": who_is_here,
        "comments": comments,
        "user_watchlist": user_watchlist
    })


def check_wl(request, listing_id):
    if not request.session.is_empty():
        user_id = request.session["user_id"]
    else:
        user_id = False

    if not user_id:
        return render(request, "auctions/listing_page.html", {
            "listing": Listing.objects.get(pk=listing_id),
            "sign_in": False
        })
    else:
        try:
            watchlist_state = Watchlist.objects.get(user_id=user_id, listing_id=listing_id)
        except Watchlist.DoesNotExist:
            watchlist_state = 0

        if watchlist_state == 0:
            Watchlist.objects.create(
                user_id=user_id,
                listing_id=listing_id,
                added=1
            )
            return redirect(f"/listing/{listing_id}")

        else:
            if watchlist_state.added == 1:
                watchlist_state.added = 0
                watchlist_state.save()
            else:
                watchlist_state.added = 1
                watchlist_state.save()

            return redirect(f"/listing/{listing_id}")


@login_required(login_url='login')
def change_bid(request, listing_id):
    new_bid = request.POST["bid"]
    user_id = request.session["user_id"]

    prev_bid = Bid.objects.get(listing_id=listing_id)
    if float(new_bid) <= float(prev_bid.bid):
        return redirect(reverse("listing_with_bid", kwargs={
            "listing_id": listing_id,
            "bid_status": "LessOrEqual"
        }))

    else:
        prev_bid.user_id = user_id
        prev_bid.bid = new_bid
        prev_bid.save()
        return redirect(reverse("listing_with_bid", kwargs={
            "listing_id": listing_id,
            "bid_status": "200"
        }))


def close_an_auction(request, listing_id):
    # close listing
    listing = Listing.objects.get(pk=listing_id)
    listing.active = False
    listing.save()

    # close bid
    bid = Bid.objects.get(listing_id=listing_id)
    bid.active = False
    bid.save()

    return redirect(reverse("index"))


@login_required(login_url='login')
def closed_auctions(request):
    user_id = request.session["user_id"]

    # check for user watchlist items
    try:
        user_watchlist = Watchlist.objects.filter(user_id=user_id, added=True)
    except Exception:
        user_watchlist = []

    won_actions = []
    won_bids = Bid.objects.filter(user_id=user_id, active=False)
    for bid in won_bids:
        won_actions.append(Listing.objects.get(pk=bid.listing_id))

    return render(request, 'auctions/closed_auctions.html', {
        "won_auctions": won_actions,
        "closed_auction_list": Listing.objects.filter(user=user_id, active=False),
        "user_watchlist": user_watchlist
    })


@login_required(login_url='login')
def add_comment(request, listing_id):
    user_id = request.session["user_id"]

    # if comment is empty, send the error message
    comment = request.POST["comment"]
    if not comment:
        return redirect(f"/listing/{listing_id}")

    # otherwise add the comment
    comment = Comment.objects.create(
        listing_id=listing_id,
        user_id=User.objects.get(id=user_id),
        comment=comment
    )

    return redirect(f"/listing/{listing_id}")


@login_required(login_url='login')
def watchlist(request):
    user_id = request.session["user_id"]

    watchlist_items = Watchlist.objects.filter(user_id=user_id, added=True)
    related_listing = []
    for item in watchlist_items:
        related_listing.append(Listing.objects.get(pk=item.listing_id))
    return render(request, "auctions/watchlist.html", {
        "watchlist_items": related_listing
    })


def categories(request):
    # check for user watchlist items
    try:
        user_id = request.session["user_id"]
        user_watchlist = Watchlist.objects.filter(user_id=user_id, added=True)
    except Exception:
        user_watchlist = []

    category_listing = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": category_listing,
        "user_watchlist": user_watchlist
    })


def category_listings(request, category_name):
    # check for user watchlist items
    try:
        user_id = request.session["user_id"]
        user_watchlist = Watchlist.objects.filter(user_id=user_id, added=True)
    except Exception:
        user_watchlist = []

    related_listing = Listing.objects.filter(cats=category_name, active=True)
    return render(request, "auctions/category_listings.html", {
        "listings": related_listing,
        "cat_name": Category.objects.get(id=category_name),
        "user_watchlist": user_watchlist
    })
