# tourism/templatetags/tourism_tags.py
from django import template

register = template.Library()

@register.filter
def get_primary_image(attraction):
    """Get primary image or first image for an attraction"""
    primary = attraction.images.filter(is_primary=True).first()
    if primary:
        return primary
    return attraction.images.first()

@register.filter
def get_image_url(attraction):
    """Get image URL for an attraction"""
    image = get_primary_image(attraction)
    if image:
        return image.image_url
    return None