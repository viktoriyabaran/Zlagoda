def resolve_sort(request, sortable, default=None):
    sort_by = request.GET.get("sort") or default
    if sort_by not in sortable:
        sort_by = default
    sort_dir = request.GET.get("dir", "asc").lower()
    if sort_dir not in ("asc", "desc"):
        sort_dir = "asc"
    return sort_by, sort_dir


def order_by_sql(sort_by, sort_dir):
    if not sort_by:
        return ""
    direction = "DESC" if sort_dir == "desc" else "ASC"
    return f" ORDER BY {sort_by} {direction}"
