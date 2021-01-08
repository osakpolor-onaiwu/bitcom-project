from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.db import connection

# Create your views here.


def dictfetchall(cursor):
    desc = cursor.description
    return[
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


def index(request):
    cursor = connection.cursor()
    query = """select apus.polling_unit_uniqueid ,apus.party_abbreviation,apus.party_score,
     (select pu.polling_unit_name from votersapplication.polling_unit pu where pu.uniqueid = 
     (select uniqueid from votersapplication.polling_unit where votersapplication.polling_unit.uniqueid = apus.polling_unit_uniqueid)) 
     polling_unit_name,(select w.ward_name from votersapplication.ward w where w.uniqueid = 
     (select uniquewardid from votersapplication.polling_unit where votersapplication.polling_unit.uniqueid = apus.polling_unit_uniqueid)) ward_name,
     (select l.lga_name from votersapplication.lga l where l.lga_id = 
     (select lga_id from votersapplication.polling_unit where votersapplication.polling_unit.uniqueid = apus.polling_unit_uniqueid))
      lga from votersapplication.announced_pu_results apus"""
    cursor.execute(query
                   )
    r = dictfetchall(cursor)

    print(connection.queries)
    return render(request, 'poll/index.html', {'data': r})
