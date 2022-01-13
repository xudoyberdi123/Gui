# -*- coding: utf-8 -*-
from contextlib import closing
from collections import OrderedDict
from django.db import connection
from django.conf import settings

from base import StatusChoice
from base.db import dictfetchall, dictfetchone
from base.sqlpaginator import SqlPaginator

PER_PAGE = settings.PAGINATE_BY


def get_list(request):
    try:
        page = int(request.GET.get('page', 1))
    except:
        page = 1
    offset = (page - 1) * PER_PAGE

    extra_sql = """
    select gr.id, gr.active_status, gr."name", gr.start_date, gr.end_date, gr.start_time, gr.end_time, 
    gr.price_month, asist.firstname as assist_name,  asist.lastname as assist_last, asist.middlename as assist_mid, 
    course."name", teacher.firstname as teacher_name,  teacher.lastname as teacher_last, teacher.middlename as teacher_mid
    from education_group gr
    left join company_member asist ON asist.id = gr.assistant_id
    left join education_course course on course.id = gr.course_id
    left join company_member teacher ON teacher.id = gr.teacher_id 
    where gr.active_status=2
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
            "SELECT count(1) as cnt FROM education_group where active_status=2")
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
    select gr.id, gr.active_status, gr."name", gr.start_date, gr.end_date, gr.start_time, gr.end_time, 
    gr.price_month,asist.id as assist_id, asist.firstname as assist_name,  asist.lastname as assist_last, asist.middlename as assist_mid, 
    course."name",teacher.id as teacher_id, teacher.firstname as teacher_name,  teacher.lastname as teacher_last, 
    teacher.middlename as teacher_mid
    from education_group gr
    left join company_member asist ON asist.id = gr.assistant_id
    left join education_course course on course.id = gr.course_id
    left join company_member teacher ON teacher.id = gr.teacher_id 
    where gr.id=%s and gr.active_status=2

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
    if data['assist_id']:
        assist = OrderedDict([
            ('id', data['assist_id']),
            ('name', data['assist_name']),
            ('lastname', data['assist_last']),
            ('middlename', data['assist_mid']),
        ])
    else:
        assist = None

    if data['teacher_id']:
        teacher = OrderedDict([
            ('id', data['teacher_id']),
            ('name', data['teacher_name']),
            ('lastname', data['teacher_last']),
            ('middlename', data['teacher_mid']),
        ])
    else:
        teacher = None

    if data['active_status']:
        status = StatusChoice.getValue(data['active_status'])
    else:
        status = None

    return OrderedDict([
        ('id', data['id']),
        ('teacher', teacher),
        ('assist', assist),
        ('status', status),
        ('start_date', data['start_date']),
        ('end_date', data['end_date']),
        ('start_time', data['start_time']),
        ('end_time', data['end_time']),
        ('price', data['price_month']),
    ])
