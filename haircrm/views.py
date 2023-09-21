from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from .models import Worker, Client, Client_data, Cita
from django.contrib.auth.decorators import login_required
import datetime

def home(request):
    return redirect('/schedule')

# ------------ WORKERS ------------
@login_required
def workers(request):
    if request.method == 'POST':
        nevo_worker = Worker(nombre=request.POST['nombre'])
        try:
            nevo_worker.save()
        except:
            return HttpResponse("<h1>ERROR creating worker, it might exist</h1>")
    workers = Worker.objects.all()
    return render(request,'workers.html',{
        'workers': workers,
    })

@login_required
def workers_delete(request):
    if request.GET['id']:
        try:
            workerOriginal = Worker.objects.get(id = request.GET['id'])
            workerOriginal.delete()
        except Exception as e:
            return HttpResponse("ERROR in delete")

    return redirect('./workers')

@login_required
def worker_edit(request):
    if request.method == "GET" and request.GET['id']:
        try:
            workerOriginal = Worker.objects.get(id = request.GET['id'])
            return render(request,"edit_worker.html",{ 'worker':workerOriginal })
        except Exception as e:
            return HttpResponse("ERROR in Edit")
    else:
        try:
            workerOriginal = Worker.objects.get(id = request.GET['id'])
            if request.POST["nombre"]:
                workerOriginal.nombre = request.POST["nombre"]
                workerOriginal.save()
            return redirect("./workers")
        except Exception as e:
            return HttpResponse("ERROR in Edit")

# ------------ CLIENTS ------------
@login_required
def clients(request):
    if request.method == 'POST':
        nevo_cliente = Client(nombre=request.POST['nombre'],telefono = request.POST['telefono'])
        try:
            nevo_cliente.save()
        except:
            return HttpResponse("<h1>ERROR creating client, it might exist</h1>")
    clients = Client.objects.all()
    return render(request,'clients.html',{
        'clients': clients,
    })

@login_required
def clients_delete(request):
    if request.GET['id']:
        try:
            client = Client.objects.get(id = request.GET['id'])
            client.delete()
        except Exception as e:
            return HttpResponse("ERROR in delete")
    return redirect('./clients')

@login_required
def client_edit(request):
    if request.method == "GET" and request.GET['id']:
        try:
            client = Client.objects.get(id = request.GET['id'])
            return render(request,"edit_client.html",{ 'client':client })
        except Exception as e:
            return HttpResponse("ERROR in Edit")
    else:
        try:
            client = Client.objects.get(id = request.GET['id'])
            if request.POST["nombre"] and request.POST['telefono']:
                client.nombre = request.POST["nombre"]
                client.telefono = request.POST["telefono"]
                client.save()
            return redirect("./clients")
        except Exception as e:
            print(e)
            return HttpResponse("ERROR in Edit")

# ------------ CLIENTS DATA ------------
@login_required
def client_data(request):
    if request.method == 'POST':
        try:
            client_o = Client.objects.get(id = request.GET['id'])
            nevo_cliente = Client_data(data=request.POST['data'],client=client_o)
            nevo_cliente.save()
        except:
            return HttpResponse("<h1>ERROR creating client, it might exist</h1>")
    if request.GET['id']:
        client = Client.objects.get(id = request.GET['id'])
        return render(request,'client_view.html',{
            'client': client,
            'client_data': client.userData.all()
        })
    else:
        redirect('./clients')
@login_required
def client_data_delete(request):
    if 'id' in request.GET:
        try:
            client_data = Client_data.objects.get(id = request.GET['id'])
            client_data.delete()
        except Exception as e:
            return HttpResponse("ERROR in delete")
    return redirect('./client_view?id='+request.GET['id'])

# ------------ SCHEDULE ------------
@login_required
def schedule(request):
    if 'day' in request.GET and 'month' in request.GET and 'year' in request.GET:
        if 'previeus' in request.GET:
            now = datetime.date(day=int(request.GET['day']),month=int(request.GET['month']),year=int(request.GET['year'])) - datetime.timedelta(days=   1)
        else:
            now = datetime.date(day=int(request.GET['day']),month=int(request.GET['month']),year=int(request.GET['year'])) - datetime.timedelta(days=-1)
        citas = Cita.objects.filter(start__year=now.year,start__month=now.month,start__day=now.day).order_by('-start')
    else:
        now = datetime.date.today()
        citas = Cita.objects.filter(start__year=now.year,start__month=now.month,start__day=now.day)

    weekDays = ['Mon','Tues','Wed','Thurds','Fri','Sat','Sun']
    return render(request,"schedule.html",{'citas': citas, 'now': now, 'weekday': weekDays[now.weekday()] })
@login_required
def booking(request):
    if request.method == 'POST':
        start = datetime.datetime(year=int(request.GET['year']),month=int(request.GET['month']),day=int(request.GET['day']),hour=int(request.POST['start']),minute=0)
        end = datetime.datetime(year=int(request.GET['year']),month=int(request.GET['month']),day=int(request.GET['day']),hour=int(request.POST['end']),minute=0)
        try:
            client = Client.objects.get(id=request.POST['clients'])
            worker = Worker.objects.get(id=request.POST['workers'])

            if 'id' in request.GET:
                cita_nueva = Cita.objects.get(id=request.GET['id'])
                cita_nueva.start = start
                cita_nueva.end = end
                cita_nueva.client = client
                cita_nueva.worker = worker
            else:
                cita_nueva = Cita(start=start,end=end,client=client,worker=worker)
            cita_nueva.save()
            return redirect("./schedule?day={}&month={}&year={}".format(int(request.GET['day'])-1,int(request.GET['month']),int(request.GET['year'])))
        except Exception as e:
            print(e)
            return HttpResponse('Error in booking')
    try:
        clients = Client.objects.all()
        workers = Worker.objects.all()
    except Exception as e:
        return HttpResponse('Error in schedule')
    date = "{}/{}/{}".format(int(request.GET['day']),int(request.GET['month']),int(request.GET['year']))
    return render(request,"booking.html",{'clients':clients, 'workers': workers, 'date': date })

@login_required
def booking_edit(request):
    try:
        cita_o = Cita.objects.get(id=request.GET['id_cita'])
        clients = Client.objects.all()
        workers = Worker.objects.all()
    except Exception as e:
        return HttpResponse('Error in schedule')
    date = "{}/{}/{}".format(int(request.GET['day']),int(request.GET['month']),int(request.GET['year']))
    return render(request,"edit_booking.html",{'clients':clients, 'workers': workers, 'date': date, 'cita_o': cita_o })
