from django.shortcuts import render, get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from .models import Listing
from .choices import bedroom_choices, price_choices, state_choices
# Create your views here.


def index(request):
    listings = Listing.objects.order_by('-list_date').filter(is_published=True)

    paginator = Paginator(listings, 6)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)

    context = {
        'listings': paged_listings
    }
    return render(request, 'listings/listings.html', context)


def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)

    context = {
        'listing': listing
    }
    return render(request, 'listings/listing.html', context)


def search(request):
    listing_query = Listing.objects.order_by('-list_date')

    # Search by keywords
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            listing_query = listing_query.filter(
                description__icontains=keywords)

    # Search by state
    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            listing_query = listing_query.filter(
                city__iexact=city)

    # Search by state
    if 'state' in request.GET:
        state = request.GET['state']
        if state:
            listing_query = listing_query.filter(
                state__iexact=state)

    # Search by bedrooms
    if 'bedrooms' in request.GET:
        bedrooms = request.GET['bedrooms']
        if bedrooms:
            listing_query = listing_query.filter(
                bedrooms__lte=bedrooms)

    # Search by price
    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            listing_query = listing_query.filter(
                price__lte=price)

    context = {
        'listing_query': listing_query,
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices,
        'state_choices': state_choices,
        'values': request.GET
    }
    return render(request, 'listings/search.html', context)
