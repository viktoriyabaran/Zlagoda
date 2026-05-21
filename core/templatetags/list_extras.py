from django import template

register = template.Library()


@register.filter
def cell(row, key):
    value = row.get(key)
    return "" if value is None else value
