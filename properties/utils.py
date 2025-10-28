from django.core.cache import cache
from .models import Property


def get_all_properties():
    """
    Get all properties from cache if available, otherwise fetch from database
    and cache for 1 hour (3600 seconds)
    """
    # Try to get properties from Redis cache
    cached_properties = cache.get('all_properties')

    if cached_properties is not None:
        # Return cached properties
        return cached_properties
    else:
        # Fetch from database if not in cache
        properties = Property.objects.all().order_by('-created_at')

        # Store in Redis cache for 1 hour (3600 seconds)
        cache.set('all_properties', properties, 3600)

        return properties
