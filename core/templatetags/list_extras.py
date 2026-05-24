from django import template
from django.urls import reverse

register = template.Library()


@register.filter
def cell(row, key):
    value = row.get(key)
    return "" if value is None else value


@register.simple_tag
def visible_actions(actions, role):
    return [a for a in (actions or []) if not a.get("roles") or role in a["roles"]]


@register.simple_tag
def action_url(action, row, row_id_key):
    return reverse(action["url_name"], args=[row[row_id_key]])
