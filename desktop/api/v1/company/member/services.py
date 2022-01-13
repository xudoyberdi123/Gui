# -*- coding: utf-8 -*-
import ast
from contextlib import closing
from collections import OrderedDict
from django.db import connection
from django.conf import settings

from base import StatusChoice, GenderChoice
from base.db import dictfetchall, dictfetchone
from base.sqlpaginator import SqlPaginator
from company import MemberChoice

PER_PAGE = settings.PAGINATE_BY


def get_list(request):
    try:
        page = int(request.GET.get('page', 1))
    except:
        page = 1
    offset = (page - 1) * PER_PAGE

    extra_sql = """
   select mem.id, mem.firstname, mem.lastname, mem.middlename, mem.social, mem.phone_number,
mem.birthday, mem.gender, mem.is_student, mem.join_date, mem.address, mem.pass_serial, mem.status,
region.name as region, district.name as district, pos.title as position

from company_member mem
left join company_position pos on pos.id = mem.position_id
left join geo_district district on district.id = mem.district_id
left join geo_region region on region.id = mem.region_id
where mem.status = 2 or mem.status=3
group by mem.id, region.name, district.name, pos.title
limit %s offset %s
"""
    with closing(connection.cursor()) as cursor:
        cursor.execute(extra_sql, [PER_PAGE, offset])
        items = dictfetchall(cursor)
        result = []
        for data in items:
            result.append(_format(data))

    with closing(connection.cursor()) as cursor:
        cursor.execute(
            "SELECT count(1) as cnt FROM company_member where status = 2 or status=3")
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


def get_one(request, root_id):
    extra_sql = """
    select mem.id, mem.firstname, mem.lastname, mem.middlename, mem.social, mem.phone_number,
mem.birthday, mem.gender, mem.is_student, mem.join_date, mem.address, mem.pass_serial, mem.status,
region.name as region, district.name as district, pos.title as position

from company_member mem
left join company_position pos on pos.id = mem.position_id
left join geo_district district on district.id = mem.district_id
left join geo_region region on region.id = mem.region_id
where mem.id = %s and (mem.status = 2 or mem.status=3)
group by mem.id, region.name, district.name, pos.title
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
    if data['status']:
        status = MemberChoice.getValue(data['status'])
    else:
        status = None

    if data['gender']:
        gender = GenderChoice.getValue(data['gender'])
    else:
        gender = None

    return OrderedDict([
        ('id', data['id']),
        ('firstname', data['firstname']),
        ('lastname', data['lastname']),
        ('middlename', data['middlename']),
        ('social', ast.literal_eval((data['social']))),
        ('phone_number', data['phone_number']),
        ('birthday', data['birthday']),
        ('gender', gender),
        ('is_student', data['is_student']),
        ('join_date', data['join_date']),
        ('address', data['address']),
        ('pass_serial', data['pass_serial']),
        ('status', status),
        ('region', data['region']),
        ('district', data['district']),
        ('position', data['position']),

    ])

