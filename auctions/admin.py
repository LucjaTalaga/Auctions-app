from django.contrib import admin
from .models import Auctions, Bids, Comments, Watchlist

# Register your models here.
admin.site.register(Auctions)
admin.site.register(Bids)
admin.site.register(Comments)
admin.site.register(Watchlist)