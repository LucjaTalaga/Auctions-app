import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from . import utils
from .models import User, Auctions, Bids, Comments, Watchlist


def index(request, category=None):
    if category is None:
        auctions = Auctions.objects.all()
    else:
        auctions = Auctions.objects.filter(category=category)
    for auction in auctions:
        auction.price = format(utils.get_actual_price(auction), '.2f')
    return render(request, "auctions/index.html", {
        "auctions": auctions
    })

login_required(login_url='login')
def listing(request, id, alert=None):
    auction = Auctions.objects.get(id=id)
    auction.price = utils.get_actual_price(auction)

    # place new bid for this listing
    if request.method == "POST":
        bid = utils.get_number(request.POST["bid"])
        if bid is None:
            alert = "Error: Your bid must be a number"
            is_bid_correct = False
        else:
            is_bid_correct = True
        if is_bid_correct and auction.price >= bid:
            alert = "Error: Your bid must be bigger than actual price"
            is_bid_correct = False

        if is_bid_correct is False:
            return HttpResponseRedirect(reverse("listing", args=(id , alert)))
        else:
            user_name = request.user.username
            logged_user = User.objects.get(username=user_name)

            new_bid = Bids(auction_id=auction, user_id=logged_user, price=bid)
            new_bid.save()
            alert= "Added new bid"
            return HttpResponseRedirect(reverse("listing", args=(id , alert)))

    # view the actual listing         
    else:
        auction.price = format(auction.price, '.2f')
        return render(request, "auctions/listing.html",{
            "auction": auction,
            "alert": alert
        })


def categories(request):
    auctions = Auctions.objects.all()
    categories = []
    for auction in auctions:
        if auction.category and auction.category not in categories:
            categories.append(auction.category)
    return render(request, "auctions/categories.html", {
        "categories": categories      
    })


@login_required(login_url='login')
def watchlist(request):

    user_name = request.user.username
    logged_user = User.objects.get(username=user_name)

    # adding or removing item to the watchlist
    if request.method == "POST":
        id=request.POST["id"]
        auction = Auctions.objects.get(id=id)
        item = Watchlist.objects.filter(auction_id=auction).filter(user_id=logged_user).first()
        if item is None:
            watched = Watchlist(auction_id=auction, user_id=logged_user)
            watched.save()
            alert = "Added item to watchlist"
        else:
            item.delete()
            alert = "Removed item from watchlist"
        return HttpResponseRedirect(reverse("listing", args=(id , alert)))
        
    else:
        watched_items = Watchlist.objects.filter(user_id=logged_user)
        return render(request, "auctions/watchlist.html", {
            "items": watched_items        
        })


@login_required(login_url='login')    
def create(request, alert=None):
    # Creating new auction
    if request.method == "POST":
        print(request.POST)
        title = request.POST["title"].strip()
        bid = utils.get_number(request.POST["bid"])
        category = request.POST["category"].strip()
        img = request.POST["img"]
        response = requests.get(img)
        print(response)    
        if bid is None:
            alert = "Error: Your bid must be a number"
            return HttpResponseRedirect(reverse("create", args=(alert)))
        elif not title or not category:
            alert = "Error: Your must provide a title and category"
            return HttpResponseRedirect(reverse("create", args=(alert)))
        else:
            user_name = request.user.username
            logged_user = User.objects.get(username=user_name)
            new_auction = Auctions(name=title, category=category, photo=img, listed_by=logged_user)
            new_auction.save()
            new_bid = Bids(auction_id=new_auction, user_id=logged_user, price=bid)
            new_bid.save()
            id = int(new_auction.id)
            alert = "New auction added"
            return HttpResponseRedirect(reverse("listing", args=(id, alert)))
    # Displaying creating page
    else:
        return render(request, "auctions/create.html", {
            "alert": alert
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

