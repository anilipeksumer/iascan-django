#!/usr/bin/env python


from datetime import datetime
import socket
import ipaddress
# We need to create regular expressions to ensure that the input is correctly formatted.
import re
from time import sleep
from fpdf import FPDF
import django
import pyfiglet

class PortScannerDjango:
    def __init__(self):
        self.open_ports = []
        self.capturedBanners = []
        self.hname = ""
        self.ip = ""
    
    def backenderTerminal(self,djangoIP,djangoRange,djangoVelocity):
        self.ip = ""
        self.open_ports.clear()
        self.capturedBanners.clear()
        self.hname = ""
        print("************************************************\n")
        ascii_banner= pyfiglet.figlet_format("       iascan backend")
        print(ascii_banner)
        print("************************************************")
        port_range_pattern = re.compile("([0-9]+)-([0-9]+)")

        port_range_valid = port_range_pattern.search(djangoRange.replace(" ",""))
        if port_range_valid:
            startPort = int(port_range_valid.group(1))
            endPort = int(port_range_valid.group(2)) + 1
               
        if djangoVelocity == 'T1':
            timeout = 1  
        elif djangoVelocity == 'T2':
            timeout = 0.8
        elif djangoVelocity == 'T3':
            timeout = 0.6
        elif djangoVelocity == 'T4':
            timeout = 0.4
        elif djangoVelocity == 'T5':
            timeout = 0.2
            
        """
                PORT SCANNER   
                                    """
        ports = list(range(startPort,endPort))
        startTime = datetime.now()
        socket.setdefaulttimeout(timeout)
        print("[*] Scanning "+djangoIP)
        print("[*] Starting Scanning at "+str(startTime))
        host = socket.gethostbyname(djangoIP)
        self.hname = djangoIP
        print("[*] IP of host: "+host)
        self.ip = host
        
        try:
            for port in ports:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                result = sock.connect_ex((host, port))
                if result == 0:
                    print("Port {}: \t Open".format(port))
                    self.open_ports.append(port)
                sock.close()
            
        except socket.gaierror:
            return print('Hostname could not be resolved. Exiting')
        except socket.error:
            return print("Couldn't connect to server")

        endTime = datetime.now()
        totalTime = startTime - endTime
        print("[*] Scanning ended at: "+str(endTime)+"\n")
        print("[*] Time taken= "+str(totalTime))
        """
                BANNER GRABBER   
                                    """
        for port in self.open_ports:
            try:
                bannergrabber = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                bannergrabber.connect((host, port))
                bannergrabber.send('message.\r\n'.encode())
                banner = bannergrabber.recv(1245).decode()
                bannergrabber.close()
                print(f"[#] Banner Found: \n{banner}")
                self.capturedBanners.append(f"Port = {port}, Banner = {banner}")
                print("-" * 60)
            except:
                pass 
        # self.createPDF()

        
    def createPDF(self): # pip install FPDF
        date = str(datetime.date(datetime.now())) + " "
        time = str(datetime.time(datetime.now()))
        fileName = '[' + str(self.hname) +'] ' + date + time + " Scan Report.pdf"
             
        from reportlab.pdfgen import canvas
        from reportlab.lib.units import inch  
              
        my_canvas = canvas.Canvas(fileName,bottomup=0)
        my_canvas.drawString(45,45,"iascan Result")
        my_canvas.drawImage("static/logo-tsp.jpg",6*inch,0.2*inch,45,45)
        my_canvas.drawString (45,120,"Open Ports:")
        position = 140
        for port in self.open_ports:
            my_canvas.drawString(45, position, str(port))
            position = position + 20
            if port == 80:
                flag = 0
                for banner in self.capturedBanners:
                    if "Port = 80," in banner and "Server:" in banner:
                        print('BURADAYIM')
                        starting = str(banner).index("Server:")
                        bg = str(banner)[starting:]
                        ending = bg.index("\r\n")
                        bg = bg[:ending]
                        print(bg)
                        bg = 'Web ' + bg 
                        flag = 1
                if flag == 0:
                    bg = 'Web Server : - '
                    
                my_canvas.drawString(80, position - 20, bg)


        
        # position = position + 40
        
        # my_canvas.drawString (45,position ,"Grabbed Banners:")
        # position = position + 20
        
        my_canvas.save()



        
        