from django import template
register = template.Library()

@register.filter
def pluck(objects, key):
    return [obj.get(key) for obj in objects]

def sum_field(queryset, field_name):
    return sum(getattr(obj, field_name, 0) for obj in queryset)
