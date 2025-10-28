from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from .utils import get_all_properties


@cache_page(60 * 15)  # Cache the entire response for 15 minutes
def property_list(request):
    """
    View to return all properties as JSON
    Uses low-level cache for queryset (1 hour) and page cache for response (15 minutes)
    """
    # Use the utility function that implements low-level caching
    properties = get_all_properties()

    # Convert properties to dictionary format
    properties_data = [
        {
            'id': property.id,
            'title': property.title,
            'description': property.description,
            'price': str(property.price),  # Convert Decimal to string for JSON
            'location': property.location,
            'created_at': property.created_at.isoformat()
        }
        for property in properties
    ]

    return JsonResponse({
        'data': properties_data,
        'count': len(properties_data),
        'status': 'success'
    })
