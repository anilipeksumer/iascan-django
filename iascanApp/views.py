from email import message, message_from_string
from ipaddress import ip_address
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
globalPortScannerObject = capturedLists()

class capturedDirs:
    def __init__(self):
        self.dirs = []
        self.hostname = ""
        self.ip = ""
        self.count = 0
globalDirBusterObject = capturedDirs()

def index(request):
    return render(request=request, template_name="index.html")

def portScan(request):
    return render(request=request, template_name="portscan.html")

def about(request):
    return render(request=request, template_name="about.html")

def addScan (request):
    form = ScannerForm(request.POST or None)
    if form.is_valid():
        # If method is POST do XSS, type, scalarity controls.
        disallowedchars = ["<", ">", "?", "\'", "=", "(", ")", "[" ,"]", "+", "-", "{", "}", "{", "}", "%", "&", "#", ";", "@", "|","\"","\\"]
        for char in disallowedchars:
            if char in request.POST['domainName']:
                return HttpResponse("<h1>Unallowed Characters!</h1><br> Special characters are not allowed! (eg. >, <, =, etc...)")
            elif char in request.POST['startPort']:
                return HttpResponse("<h1>Unallowed Characters!</h1><br> Special characters are not allowed! (eg. >, <, =, etc...)")
            elif char in request.POST['endPort']:
                return HttpResponse("<h1>Unallowed Characters!</h1><br> Special characters are not allowed! (eg. >, <, =, etc...)")
        startPort = int(request.POST['startPort'])
        endPort = int(request.POST['endPort'])
        if startPort > endPort or startPort < 0 or endPort < 0 or startPort > 65535 or endPort > 65535:
            return HttpResponse("<h1>400 Bad Request</h1><br><h2>Check your Port Numbers!</h2><h3>Port numbers can between 0-65535!</h3> <h3> EndPort must be bigger than StartPort")
        
        # If the variables are fine, start process.
        formObject = form.save(commit = False) # Do not commit, because ip and scan date fields are going to be added to system.
        messages.success(request,"Port Scan is started.") # Admin panel success message.
        portScannerObject = portscanner.PortScannerDjango() # Create portscanner object to scan open ports.
        portScannerObject.backenderTerminal(request.POST['domainName'],request.POST['startPort'],request.POST['endPort'],request.POST['velocityField'])
        if request.POST['domainName'] == "app.iascan.online":
                return HttpResponse("<h1>400 Bad Request</h1><br><h3>app.iascan.online is not avaliable for scanning!</h3>")
        globalPortScannerObject.ports = portScannerObject.open_ports
        globalPortScannerObject.banners = portScannerObject.capturedBanners
        globalPortScannerObject.hostname = portScannerObject.hname
        globalPortScannerObject.ip = portScannerObject.ip
        formObject.ipField = portScannerObject.ip
        formObject.ports = globalPortScannerObject.ports
        formObject.banners = globalPortScannerObject.banners
        formObject.save()
        database = PortScanner.objects.last()
        id = database.pk + 1
        id = str(id)
        # del portScannerObject, form, formObject, database
        return HttpResponseRedirect('/results/{}'.format(id))
    else:    
        return render(request,"startScan.html",{"form":form})
    
def dbuster(request):
    form = DirForm(request.POST or None)
    # POST method validation and XSS control.
    if form.is_valid():
        disallowedchars = ["<", ">", "?", "\'", "=", "(", ")", "[" ,"]", "+", "-", "{", "}", "{", "}", "%", "&", "#", ";", "@", "|","\"","\\"]
        for char in disallowedchars:
            if char in request.POST['domainName']:
                return HttpResponse("<h1>Unallowed Characters!</h1><br> Special characters are not allowed! (eg. >, <, =, etc...)")
        if request.POST['domainName'] == "app.iascan.online":
                return HttpResponse("<h1>400 Bad Request</h1><br><h3>app.iascan.online is not avaliable for scanning!</h3>")
            # If variables are true
        messages.success(request,"Port Scan is started.")
        dirBusterObject = dirbuster.DirBusterDjango()
        dirBusterObject.backendTerminal(request.POST['domainName'], request.POST['sslField'])
        globalDirBusterObject.dirs = dirBusterObject.returnedDirs
        globalDirBusterObject.hostname = request.POST['domainName']
        form.save()
        database = DirBuster.objects.last()
        id = database.pk + 1
        id = str(id)
        return HttpResponseRedirect('/dirbresults/{}'.format(id))
    else:    
        return render(request,"dirbuster.html",{"form":form})

def results(request,id):
    context = {"hostname":globalPortScannerObject.hostname, "ip":globalPortScannerObject.ip,"ports":globalPortScannerObject.ports, "banners":globalPortScannerObject.banners}
    return render(request,"results.html",context)

def dirbresults(request,id):
    context = {"hostname":globalDirBusterObject.hostname, "dirs": globalDirBusterObject.dirs}
    return render(request,"dirbresults.html",context)

