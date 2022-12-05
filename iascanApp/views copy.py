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

# Create your views here.
#URL GELDİĞİNDE ÇALIŞACAK FONKSİYONLAR
class capturedLists:
    def __init__(self):
        self.ports = []
        self.banners = []
listObject = capturedLists()

class capturedDirs:
    def __init__(self):
        self.dirs = []
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
        messages.success(request,"Port Scan is started.")
        newObject = portscanner.PortScannerDjango()
        newObject.backenderTerminal(request.POST['domainName'],request.POST['portRange'],request.POST['velocityField'])
        listObject.ports = newObject.open_ports
        listObject.banners = newObject.capturedBanners
       
        return HttpResponseRedirect('/results/')
    else:    
        return render(request,"startScan.html",{"form":form})
    
def dbuster(request):
    form = DirForm(request.POST or None)
    if form.is_valid():
        messages.success(request,"Port Scan is started.")
        newObject = dirbuster.DirBusterDjango()
        newObject.backendTerminal(request.POST['domainName'], request.POST['sslField'])
        dirListObject.dirs = newObject.returnedDirs
        return HttpResponseRedirect('/dirbresults/')
    else:    
        return render(request,"dirbuster.html",{"form":form})

    #     object = form.save(commit=False)
    #     ip_address = (socket.gethostbyname(object.get))
       
    # return render(request,"startScan.html",{"form":form})

def results(request):
    return render(request,"results.html",{"ports":listObject.ports, "banners":listObject.banners})

def dirbresults(request):
    return render(request,"dirbresults.html",{"dirs":dirListObject.dirs})

