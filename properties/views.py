from django.shortcuts import render
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from .models import Property


@cache_page(60 * 15)  # Cache for 15 minutes
def property_list(request):
    """
    View to display all properties with response cached for 15 minutes
    """
    properties = Property.objects.all().order_by('-created_at')

    context = {
        'properties': properties,
        'total_properties': properties.count()
    }

    return render(request, 'properties/property_list.html', context)
