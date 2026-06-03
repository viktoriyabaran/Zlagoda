from django import template
from django.urls import reverse

register = template.Library()


@register.filter
def cell(row, key):
    value = row.get(key)
    return "" if value is None else value


@register.filter
def query_value(get, key):
    return get.get(key, "")


@register.simple_tag
def filters_of(filters, kind):
    if kind == "search":
        return [f for f in (filters or []) if f.get("type") == "search"]
    return [f for f in (filters or []) if f.get("type") != "search"]


@register.simple_tag(takes_context=True)
def any_filter_value(context, filters):
    get = context["request"].GET
    return any(get.get(f["key"]) for f in (filters or []))


@register.simple_tag(takes_context=True)
def query_without(context, *keys):
    params = context["request"].GET.copy()
    for key in keys:
        params.pop(key, None)
    return params.urlencode()


@register.simple_tag
def visible_actions(actions, role):
    return [a for a in (actions or []) if not a.get("roles") or role in a["roles"]]


@register.simple_tag
def action_url(action, row, row_id_key):
    return reverse(action["url_name"], args=[row[row_id_key]])
