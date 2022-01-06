# -*- coding: utf-8 -*-
from contextlib import closing
from collections import OrderedDict
from django.db import connection

from base.db import dictfetchall
from base.sqlpaginator import SqlPaginator


def get_region_list(request):
    rows = _get_regions()
    result = []
    for data in rows:
        result.append(OrderedDict([
            ('id', data['id']),
            ('name', data['name'])
        ]))
    paginator = SqlPaginator(request, page=1, per_page=len(result), count=len(result))
    pagging = paginator.get_paginated_response()
    return OrderedDict([
        ('items', result),
        ('meta', pagging)
    ])

def get_district_list(request, id=None):
    rows = _get_districts(id)
    result = []
    for data in rows:
        result.append(OrderedDict([
            ('id', data['id']),
            ('region_id', data['region_id']),
            ('name', data['name'])
        ]))
    paginator = SqlPaginator(request, page=1, per_page=len(result), count=len(result))
    pagging = paginator.get_paginated_response()
    return OrderedDict([
        ('items', result),
        ('meta', pagging)
    ])


def _get_regions():
    extra_sql = """select id, name FROM geo_region ORDER BY ordering LIMIT 100"""
    with closing(connection.cursor()) as cursor:
        cursor.execute(extra_sql)
        rows = dictfetchall(cursor)
    return rows

def _get_districts(region_id):
    extra_sql = "select id, region_id, name FROM geo_district WHERE region_id = %s ORDER BY ordering LIMIT 100"
    with closing(connection.cursor()) as cursor:
        cursor.execute(extra_sql, [region_id])
        rows = dictfetchall(cursor)
    return rows
