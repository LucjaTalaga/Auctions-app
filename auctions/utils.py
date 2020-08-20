

def get_actual_price(auction):
    bids = auction.auction_bids.all()
    max_bid = bids.order_by('-price').first()
    price = round(max_bid.price, 2)
    return price 

def get_number(bid):
    try:
        return float(bid)
    except ValueError:
        return None