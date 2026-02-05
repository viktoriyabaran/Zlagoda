"""
Raw SQL utilities for database operations.

All data queries must use these utilities instead of Django ORM.
Django ORM is ONLY used for model definitions and migrations.
"""
from django.db import connection


def execute_query(sql, params=None):
    """Execute a SELECT query and return list of dicts."""
    with connection.cursor() as cursor:
        cursor.execute(sql, params or [])
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]


def execute_single(sql, params=None):
    """Execute a SELECT query and return a single dict or None."""
    results = execute_query(sql, params)
    return results[0] if results else None


def execute_write(sql, params=None):
    """Execute INSERT/UPDATE/DELETE and return affected row count."""
    with connection.cursor() as cursor:
        cursor.execute(sql, params or [])
        return cursor.rowcount


def execute_insert_returning(sql, params=None):
    """Execute INSERT with RETURNING clause and return the value."""
    with connection.cursor() as cursor:
        cursor.execute(sql, params or [])
        row = cursor.fetchone()
        return row[0] if row else None
