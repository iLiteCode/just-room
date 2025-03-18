from django import template

register = template.Library()

# Register as a filter
@register.filter(name='percentage')
def percentage(value, total):
    if total == 0:
        return 0  # or some other default value
    return (value / total) * 100
