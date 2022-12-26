from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.utils import timezone
from django.http import HttpResponse,FileResponse, JsonResponse
from fpdf import FPDF
import requests
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from TPapp.models import Ds18b20
from TPapp.serializer import dstser
from TPapp.serializer import dstser1
from django.shortcuts import render
import xlwt
import matplotlib
matplotlib.use('Agg')
from django.contrib.auth.models import User

def graph_mois(request):
    Maintenant= datetime.now()
    data = []
    dataalert = []
    VBAT = []
    labels = []
    labelsalert = []
    alldata = []
    alldataalert = []
    titre= "Mois"
    queryset = Ds18b20.objects.filter(dt__year=Maintenant.year, dt__month=Maintenant.month)
    for i in queryset:
        data.append(i.tmp)
        VBAT.append(i.vbat)
        labels.append(str(i.dt.strftime("%Y-%m-%d %H:%M")))
        alldata.append((i.tmp,i.vbat, str(i.dt.strftime("%Y-%m-%d %H:%M"))))
        if i.tmp > 20:
            dataalert.append(i.tmp)
            labelsalert.append(str(i.dt.strftime("%Y-%m-%d %H:%M")))
            alldataalert.append((i.tmp, str(i.dt.strftime("%Y-%m-%d %H:%M"))))
    count = len(data)
    vmax = round(max(data), 2)
    vmin = round(min(data), 2)
    vavg = round(sum(data) / len(data), 2)
    last = data[-1]
    n = 0
    for i in range(len(data) - 1, 0, -1):
        if data[i] > 20:
            n += 1
        else:
            break
    s = {'alldata': alldata, 'data': data,'vbat':VBAT, 'labels': labels, 'alldataalert': alldataalert, 'dataalert': dataalert,
         'labelsalert': labelsalert, "vmin": vmin, "vavg": vavg, "vmax": vmax, "count": count,"titre":titre, "last": last, "n": n}

    return render(request, 'graph.html', s)


# donnes de 24 heures:

def graph_24h(request):

    Maintenant=datetime.now()
    data = []
    dataalert = []
    labels = []
    VBAT = []
    labelsalert = []
    alldata = []
    alldataalert = []
    titre= "24 Heures"
    t24h = Maintenant-timedelta(hours=24)
    queryset = Ds18b20.objects.filter(dt__range=(t24h,Maintenant))
    for i in queryset:
        data.append(i.tmp)
        VBAT.append(i.vbat)
        labels.append(str(i.dt.strftime("%Y-%m-%d %H:%M")))
        alldata.append((i.tmp,i.vbat, str(i.dt.strftime("%Y-%m-%d %H:%M"))))
        if i.tmp>20:
            dataalert.append(i.tmp)
            labelsalert.append(str(i.dt.strftime("%Y-%m-%d %H:%M")))
            alldataalert.append((i.tmp, str(i.dt.strftime("%Y-%m-%d %H:%M"))))
    count=len(data)
    vmax=round(max(data),2)
    vmin=round(min(data),2)
    vavg=round(sum(data)/len(data),2)
    last=data[-1]
    n=0
    for i in range(len(data)-1,0,-1):
        if data[i]>20 :
            n+=1
        else :
            break

    s={'alldata':alldata,'data':data,'vbat':VBAT,'labels':labels,'alldataalert':alldataalert,'dataalert':dataalert,'labelsalert':labelsalert,"vmin":vmin, "vavg": vavg, "vmax":vmax, "count": count,"last":last,"n":n}

    return render(request, 'graph.html', s)

# donnes d'une heure:
def graph_heure(request):

    Maintenant= datetime.now()
    data = []
    dataalert = []
    labels =[]
    VBAT = []
    labelsalert = []
    alldata=[]
    alldataalert = []
    titre= "60 vminutes"
    une_heure = Maintenant-timedelta(hours=1)
    queryset = Ds18b20.objects.filter(dt__range=(une_heure,Maintenant))
    for i in queryset:
        data.append(i.tmp)
        VBAT.append(i.vbat)
        labels.append(str(i.dt.strftime("%Y-%m-%d %H:%M")))
        alldata.append((i.tmp,i.vbat, str(i.dt.strftime("%Y-%m-%d %H:%M"))))
        if i.tmp>20:
            dataalert.append(i.tmp)
            labelsalert.append(str(i.dt.strftime("%Y-%m-%d %H:%M")))
            alldataalert.append((i.tmp, str(i.dt.strftime("%Y-%m-%d %H:%M"))))
    count=len(data)
    vmax=round(max(data),2)
    vmin=round(min(data),2)
    vavg=round(sum(data)/len(data),2)
    last=data[-1]
    n=0
    for i in range(len(data)-1,0,-1):
        if data[i]>20 :
            n+=1
        else :
            break

    s={'alldata':alldata,'data':data,'vbat':VBAT,'labels':labels,'alldataalert':alldataalert,'dataalert':dataalert,'labelsalert':labelsalert,"vmin":vmin, "vavg": vavg, "vmax":vmax, "count": count,"last":last,"n":n}
    return render(request, 'graph.html', s)

# tout les donnes:

def graph_all(request):
    plot()
    data = []
    VBAT = []
    dataalert = []
    labels =[]
    labelsalert = []
    alldata=[]
    alldataalert = []
    queryset = Ds18b20.objects.all()
    for i in queryset:
        data.append(i.tmp)
        VBAT.append(i.vbat)
        labels.append(str(i.dt.strftime("%Y-%m-%d %H:%M")))
        alldata.append((i.tmp,i.vbat,str(i.dt.strftime("%Y-%m-%d %H:%M"))))
        if i.tmp>20:
            dataalert.append(i.tmp)
            labelsalert.append(str(i.dt.strftime("%Y-%m-%d %H:%M")))
            alldataalert.append((i.tmp, str(i.dt.strftime("%Y-%m-%d %H:%M"))))
    count=len(data)
    vmax=round(max(data),2)
    vmin=round(min(data),2)
    vavg=round(sum(data)/len(data),2)
    last=data[-1]
    n=0
    for i in range(len(data)-1,0,-1):
        if data[i]>20 :
            n+=1
            print(str(vmax))
        else :
            break

    s={'alldata':alldata,'data':data,'vbat':VBAT,'labels':labels,'alldataalert':alldataalert,'dataalert':dataalert,'labelsalert':labelsalert,"vmin":vmin, "vavg": vavg, "vmax":vmax, "count": count,"last":last,"n":n}
    return render(request, 'graph.html', s)


#

@csrf_exempt
def Temp_serializer_agregar_data(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':

        snippets = Ds18b20.objects.all()
        serializer = dstser1(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)


    elif request.method == 'POST':

        data = JSONParser().parse(request)
        serializer = dstser(data=data)
        if serializer.is_valid():
            serializer.save()

            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


##################################################################



def menu(request):
    return render(request, 'menu.html')
def test(request):
    return render(request, 'home/index.html')

import csv

data = []
labels = []
alldata = []
queryset = Ds18b20.objects.all()
for i in queryset:
    data.append(str(i.tmp))
    labels.append(str(i.dt.strftime("%Y-%m-%d %H:%M")))
    alldata.append((i.tmp,i.vbat, str(i.dt.strftime("%Y-%m-%d %H:%M"))))
DATE = labels
TMP = data


def psg(request):

    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="data.csv"'},
    )
    writer = csv.writer(response)
    writer.writerow({'Dates', 'Temperatures'})
    for (name, sub) in zip(DATE, TMP):
         writer.writerow([name, sub])
    return response



def export_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Ds18B20.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Ds18B20')
    data = []
    labels = []
    alldata = []
    queryset = Ds18b20.objects.all()
    for i in queryset:
        data.append(str(i.tmp))
        labels.append(str(i.dt.strftime("%Y-%m-%d %H:%M")))
        alldata.append((i.tmp, str(i.dt.strftime("%Y-%m-%d %H:%M"))))

    DATE = labels
    TMP = data
    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Dates', 'Temperatures', ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = alldata
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response




def report(request):
    sales = []
    data = []
    queryset = Ds18b20.objects.all()
    for i in queryset:
        data.append(float(i.tmp))
        sales.append((str(i.tmp), str(i.dt.strftime("%Y-%m-%d %H:%M"))))
    count=len(data)
    vmax=round(max(data),2)
    vmin=round(min(data),2)
    vavg=round(sum(data)/len(data),2)
    pdf = FPDF('P', 'mm', 'A4')
    pdf.add_page()
    pdf.image('logo.png')
    pdf.set_font('courier', 'B', 16)
    pdf.cell(40, 10, 'Rapport des enregistrements :', 0, 1)
    pdf.set_font('courier', '', 12)
    pdf.cell(40, 10, "La carte envoie les donnees tout les 20 minutes : ", 0, 1)
    pdf.cell(40, 10, "la valeur moyenne est : "f"{vavg}", 0, 1)
    pdf.cell(40, 10, "la valeur max est :"f"{vmax}", 0, 1)
    pdf.cell(40, 10, "la valeur min est :"f"{vmin}", 0, 1)
    pdf.cell(40, 10, "le nombre des enregistrement est :"f"{count}", 0, 1)
    pdf.cell(40, 10, "ce rapport contient le detail des valeurs hors norme enregistrees,", 0, 1)
    pdf.cell(40, 10, "veuillez consulter la partie telechargement pour telecharger les donnees ", 0, 1)
    pdf.cell(40, 10, "au format XLXS ou CSV pour usage externe. ", 0, 1)
    pdf.cell(40, 10, "sur les pages suivantes, vouz trouverez un graph et un tableau contenants ", 0, 1)
    pdf.cell(40, 10, "toutes les valeurs anormales enregistrees. ", 0, 1)
    pdf.cell(40, 10, '', 0, 1)
    pdf.set_font('courier', '', 12)
    pdf.image('foo.png')
    pdf.cell(200, 8, f"{'Date'.ljust(30)} {'Temperature'.rjust(20)}", 0, 1)
    pdf.line(10, 160, 150, 160)
    pdf.line(10, 152, 150, 152)

    for line in sales:
        if float(line[0])> 20 :
            pdf.cell(200, 8, f"{line[1].ljust(30)} {line[0].rjust(20)}", 0, 1)

    pdf.output('report.pdf', 'F')
    return FileResponse(open('report.pdf', 'rb'), as_attachment=True, content_type='application/pdf')

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def plot():
    sales = []
    data = []
    queryset = Ds18b20.objects.all()
    for i in queryset:
        data.append(float(i.tmp))
        sales.append((i.dt.strftime("%Y-%m-%d %H:%M")))
    plt.subplots(figsize=(6, 4))
    plt.plot(sales,data)
    plt.xticks(rotation=90,fontsize=4)

    plt.savefig('foo.png')

