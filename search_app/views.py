from django.shortcuts import render
from reviews.models import Restaurant
from django.db.models import Q

# Create your views here.
def searchResult(request):
    restaurants = None
    query = None
    if 'q' in request.GET:
        query = request.GET.get('q')
        restaurants = Restaurant.objects.filter(Q(name__contains=query) | Q(sorted__contains=query) | Q(region__contains=query))
    context = {
        'query': query,
        'restaurants': restaurants,
    }
    
    return render(request, 'search_app/search.html', context)
