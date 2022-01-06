# -*- coding: utf-8 -*-
from contextlib import closing
from collections import OrderedDict
from django.db import connection
from django.conf import settings

from base.db import dictfetchall, dictfetchone
from base.sqlpaginator import SqlPaginator

PER_PAGE = settings.PAGINATE_BY


def list_district(request):
    try:
        page = int(request.GET.get('page', 1))
    except:
        page = 1
    offset = (page - 1) * PER_PAGE

    extra_sql = """
    select district.id, district.name, district.ordering, district.region_id,
    region."name" as region_name
    from geo_district district 
    inner join geo_region region on district.region_id = region.id 
    
    order by district.id asc
    limit %s OFFSET %s
"""
    with closing(connection.cursor()) as cursor:
        cursor.execute(extra_sql, [PER_PAGE, offset])
        items = dictfetchall(cursor)
        result = []
        for data in items:
            result.append(_format(data))

    with closing(connection.cursor()) as cursor:
        cursor.execute(
            "SELECT count(1) as cnt FROM geo_district")
        row = dictfetchone(cursor)

    if row:
        count_records = row['cnt']
    else:
        count_records = 0

    paginator = SqlPaginator(request, page=page, per_page=PER_PAGE, count=count_records)
    pagging = paginator.get_paginated_response()
    return OrderedDict([
        ('items', result),
        ('meta', pagging)
    ])


def one_district(request, root_id):
    extra_sql = """
    select district.id, district.name, district.ordering, district.region_id,
    region."name" as region_name
    from geo_district district
    inner join geo_region region on district.region_id = region.id
    where district.id = %s

"""
    with closing(connection.cursor()) as cursor:
        cursor.execute(extra_sql, [root_id])
        data = dictfetchone(cursor)
        if data:
            result = _format(data)
        else:
            result = None
    return OrderedDict([
        ('item', result),
    ])


def _format(data):
    if data['region_id']:
        region = OrderedDict([
            ('id', data['region_id']),
            ('name', data['region_name'])
        ])
    else:
        region = None

    return OrderedDict([
        ('id', data['id']),
        ('name', data['name']),
        ('ordering', data['ordering']),
        ('region', region)
    ])
