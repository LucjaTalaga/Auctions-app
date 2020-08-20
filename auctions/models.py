from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Auctions(models.Model):
    name = models.CharField(max_length=64)
    category = models.CharField(max_length=32)
    photo = models.URLField()
    listed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listed")

    def __str__(self):
        return f"{self.name}"


class Bids(models.Model):
    auction_id = models.ForeignKey(Auctions, on_delete=models.CASCADE, related_name="auction_bids")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bids")
    price = models.FloatField()

    def __str__(self):
        return f"{self.id}"


class Comments(models.Model):
    auction_id = models.ForeignKey(Auctions, on_delete=models.CASCADE, related_name="auction_comments")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    comment = models.CharField(max_length=1024)

    def __str__(self):
        return f"{self.id}"

class Watchlist(models.Model):
    auction_id = models.ForeignKey(Auctions, on_delete=models.CASCADE, related_name="auction_watchlist")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_watchlist")
    
    def __str__(self):
        return f"{self.user_id}: {self.auction_id}"
