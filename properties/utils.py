from django.core.cache import cache
from django_redis import get_redis_connection
import logging
from .models import Property

# Set up logger
logger = logging.getLogger(__name__)


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


def get_redis_cache_metrics():
    """
    Retrieve and analyze Redis cache hit/miss metrics
    Returns a dictionary with cache statistics and hit ratio
    """
    try:
        # Get Redis connection
        redis_conn = get_redis_connection("default")

        # Get Redis INFO command output
        info = redis_conn.info()

        # Extract cache statistics
        hits = info.get('keyspace_hits', 0)
        misses = info.get('keyspace_misses', 0)
        total_commands = info.get('total_commands_processed', 0)
        connected_clients = info.get('connected_clients', 0)
        used_memory = info.get('used_memory_human', '0')

        # Calculate hit ratio (avoid division by zero)
        total_operations = hits + misses
        hit_ratio = hits / total_operations if total_operations > 0 else 0

        # Prepare metrics dictionary
        metrics = {
            'keyspace_hits': hits,
            'keyspace_misses': misses,
            'total_operations': total_operations,
            'hit_ratio': round(hit_ratio, 4),
            'hit_percentage': round(hit_ratio * 100, 2),
            'total_commands_processed': total_commands,
            'connected_clients': connected_clients,
            'used_memory': used_memory,
            'cache_health': 'Excellent' if hit_ratio > 0.8 else 'Good' if hit_ratio > 0.6 else 'Poor'
        }

        # Log the metrics
        logger.info(
            f"Redis Cache Metrics - "
            f"Hits: {hits}, Misses: {misses}, "
            f"Hit Ratio: {metrics['hit_percentage']}%, "
            f"Health: {metrics['cache_health']}"
        )

        return metrics

    except Exception as e:
        # Log error and return empty metrics
        logger.error(f"Error retrieving Redis cache metrics: {str(e)}")
        return {
            'error': str(e),
            'keyspace_hits': 0,
            'keyspace_misses': 0,
            'total_operations': 0,
            'hit_ratio': 0,
            'hit_percentage': 0,
            'cache_health': 'Error'
        }
