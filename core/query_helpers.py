from typing import Iterable

from django.http import HttpRequest


def resolve_sort(
    request: HttpRequest,
    sortable: Iterable[str],
    default: str | None = None,
) -> tuple[str | None, str]:
    sort_by = request.GET.get("sort") or default
    if sort_by is None or sort_by not in sortable:
        sort_by = default
    sort_dir = request.GET.get("dir", "asc").lower()
    if sort_dir not in ("asc", "desc"):
        sort_dir = "asc"
    return sort_by, sort_dir


def order_by_sql(sort_by: str | None, sort_dir: str | None) -> str:
    if not sort_by:
        return ""
    direction = "DESC" if sort_dir == "desc" else "ASC"
    return f" ORDER BY {sort_by} {direction}"


def resolve_filters(
    request: HttpRequest,
    filters: list[dict],
) -> tuple[dict[str, str], str, list[str]]:
    applied: dict[str, str] = {}
    clauses: list[str] = []
    params: list[str] = []
    for f in filters:
        raw = (request.GET.get(f["key"]) or "").strip()
        if not raw:
            continue
        if f["type"] == "select":
            if raw not in {o["value"] for o in f["options"]}:
                continue
            clauses.append(f"{f['column']} = %s")
            params.append(raw)
        elif f["type"] == "search":
            clauses.append(f"{f['column']} ILIKE %s")
            params.append(f"%{raw}%")
        applied[f["key"]] = raw
    where_sql = (" WHERE " + " AND ".join(clauses)) if clauses else ""
    return applied, where_sql, params
