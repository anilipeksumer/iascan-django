from email import message, message_from_string
from ipaddress import ip_address
from re import template
import re
import socket
from django.shortcuts import HttpResponse, HttpResponseRedirect, render,redirect
from django.contrib import messages
from . import portscanner
from . import dirbuster
from .forms import *
from .models import *

# Create your views here.
#URL GELDİĞİNDE ÇALIŞACAK FONKSİYONLAR
class capturedLists:
    def __init__(self):
        self.ports = []
        self.banners = []
        self.hostname = ""
        self.ip = ""
listObject = capturedLists()

class capturedDirs:
    def __init__(self):
        self.dirs = []
        self.hostname = ""
        self.ip = ""
dirListObject = capturedDirs()

def index(request):
    #return HttpResponse("iascan")
    return render(request=request, template_name="index.html")

def portScan(request):
    #return HttpResponse("iascan")
    return render(request=request, template_name="portscan.html")

def about(request):
    return render(request=request, template_name="about.html")

def addScan (request):
    form = ScannerForm(request.POST or None)
    if form.is_valid():
    #print(request.POST['domainName'])
        formObject = form.save(commit = False)
        messages.success(request,"Port Scan is started.")
        newObject = portscanner.PortScannerDjango()
        newObject.backenderTerminal(request.POST['domainName'],request.POST['portRange'],request.POST['velocityField'])
        listObject.ports = newObject.open_ports
        listObject.banners = newObject.capturedBanners
        listObject.hostname = newObject.hname
        listObject.ip = newObject.ip
        formObject.ipField = newObject.ip
        formObject.ports = listObject.ports
        formObject.banners = listObject.banners
        formObject.save()
        database = PortScanner.objects.last()
        print(database.pk)
        id = database.pk + 1
        id = str(id)
        return HttpResponseRedirect('/results/{}'.format(id))
    else:    
        return render(request,"startScan.html",{"form":form})
    
def dbuster(request):
    form = DirForm(request.POST or None)
    if form.is_valid():
        messages.success(request,"Port Scan is started.")
        newObject = dirbuster.DirBusterDjango()
        newObject.backendTerminal(request.POST['domainName'], request.POST['sslField'])
        dirListObject.dirs = newObject.returnedDirs
        dirListObject.hostname = request.POST['domainName']
        form.save()
        database = DirBuster.objects.last()
        id = database.pk + 1
        id = str(id)
        return HttpResponseRedirect('/dirbresults/{}'.format(id))
    else:    
        return render(request,"dirbuster.html",{"form":form})

    #     object = form.save(commit=False)
    #     ip_address = (socket.gethostbyname(object.get))
       
    # return render(request,"startScan.html",{"form":form})
def results(request,id):
    context = {"hostname":listObject.hostname, "ip":listObject.ip,"ports":listObject.ports, "banners":listObject.banners}
    return render(request,"results.html",context)


# def results(request, id):
#     return render(request,"results.html",{"ports":listObject.ports, "banners":listObject.banners})

def dirbresults(request,id):
    context = {"hostname":dirListObject.hostname, "dirs": dirListObject.dirs}
    return render(request,"dirbresults.html",context)

