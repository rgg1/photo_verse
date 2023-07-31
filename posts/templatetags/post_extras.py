from django import template
from posts.models import Like

register = template.Library()

@register.filter
def has_liked(user, post):
    return Like.objects.filter(user=user, post=post).exists()