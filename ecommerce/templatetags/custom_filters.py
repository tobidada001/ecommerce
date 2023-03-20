from django import template

register = template.Library()

@register.filter
def distinct_values(queryset, field):
    return queryset.values_list(field, flat=True).distinct()