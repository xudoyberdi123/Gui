# -*- coding: utf-8 -*-
from contextlib import closing
from collections import OrderedDict
from django.db import connection
from django.conf import settings

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
    select gr.id, gr.active_status, gr.joined_date, gr.leave_date, 
    st.firstname, st.lastname, st.middlename, gruop."name" 
    from education_groupstudent gr
    left join education_group gruop on gruop.id = gr.group_id
    left join company_member st on st.id = gr.student_id 
    where gr.active_status=2
    limit %s offset %S
"""
    with closing(connection.cursor()) as cursor:
        cursor.execute(extra_sql, [PER_PAGE, offset])
        items = dictfetchall(cursor)
        result = []
        for data in items:
            result.append(_format(data))

    with closing(connection.cursor()) as cursor:
        cursor.execute(
            "SELECT count(1) as cnt FROM education_groupstudent where active_status=2 ")
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
    
    select gr.id, gr.active_status, gr.joined_date, gr.leave_date, 
    st.firstname, st.lastname, st.middlename, gruop."name" 
    from education_groupstudent gr
    left join education_group gruop on gruop.id = gr.group_id
    left join company_member st on st.id = gr.student_id 
    where active_status=2 and id=%s
 
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
    return OrderedDict([
        ('id', data['id']),
        ('name', data['name']),
        ('ordering', data['ordering'])
    ])
