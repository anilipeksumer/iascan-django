"""_Bu sınıf, bir IP adresi, başlangıç ve bitiş portları ve hız parametrelerini alan bir port tarama ve ağ başlığı (banner) tarama
işlevini gerçekleştirir. Tarama sonuçları open_ports, capturedBanners ve ip değişkenlerine kaydedilir. init metodu, bu değişkenleri 
oluşturur ve backenderTerminal metodu tarama işlemini gerçekleştirir.
Tarama hızı, "djangoVelocity" parametresine göre ayarlanabilir ve tarama sırasında ekrana bazı bilgi mesajları yazdırılabilir.
    """

#!/usr/bin/env python
from datetime import datetime
import socket
# We need to create regular expressions to ensure that the input is correctly formatted.
import pyfiglet

class PortScannerDjango:
    def __init__(self):
        self.open_ports = []
        self.capturedBanners = []
        self.hname = ""
        self.ip = ""
    
    def backenderTerminal(self,djangoIP,djangoStartPort,djangoEndPort,djangoVelocity):
        # Tarama sırasında açık olan portları tutan liste
        startPort = int(djangoStartPort)
        endPort = int(djangoEndPort)
        # Girilen port numaralarının tip kontrolü
        if type(startPort) == "<class \'int\'>" or type(endPort) == "<class \'int\'>":
            raise ValueError
        self.ip = ""
        self.open_ports.clear()
        self.capturedBanners.clear()
        self.hname = ""
        # Terminalde bastırılacak olan ascii bannerın hazırlanması.
        print("************************************************\n")
        ascii_banner= pyfiglet.figlet_format("       iascan backend")
        print(ascii_banner)
        print("************************************************")
        
        # Kullanıcının farklı hız seçeneklerini seçmesi durumunda tarama hızının adjust edilmesi.
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
        """Taranan Portları al
        Geçen süreyi hesapla.
        Verilen domain adresinin IP'sini bul ve objeye ekle.
        Kullanıcıdan alınan port aralığındaki tüm portlara tek tek bağlanmaya çalış.
        Bağlanabildiğim portları listeye ekle.
        Hatalar için exceptionlar yer almaktadır.
        
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
                                    
        """
        Port Scannerda yakalanmış her bir port için o porta ait banner'ı yakalamaya çalış.
        Eğer banner yakalanabilirse listeye ekle.
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

            """
            Bu bölümün aşağısında yer alan kod gelecek hedeflerimizdeki pdf raporu oluşturma aşamasının ilk adımlarıdır.
            Aktif olarak çok basit bir rapor halinde çıkartıldığından ana projeye henüz dahil edilmemiştir.
            """
        
    # def createPDF(self): # pip install FPDF
    #     date = str(datetime.date(datetime.now())) + " "
    #     time = str(datetime.time(datetime.now()))
    #     fileName = '[' + str(self.hname) +'] ' + date + time + " Scan Report.pdf"
             
    #     from reportlab.pdfgen import canvas
    #     from reportlab.lib.units import inch  
              
    #     my_canvas = canvas.Canvas(fileName,bottomup=0)
    #     my_canvas.drawString(45,45,"iascan Result")
    #     my_canvas.drawImage("static/logo-tsp.jpg",6*inch,0.2*inch,45,45)
    #     my_canvas.drawString (45,120,"Open Ports:")
    #     position = 140
    #     for port in self.open_ports:
    #         my_canvas.drawString(45, position, str(port))
    #         position = position + 20
    #         if port == 80:
    #             flag = 0
    #             for banner in self.capturedBanners:
    #                 if "Port = 80," in banner and "Server:" in banner:
    #                     print('BURADAYIM')
    #                     starting = str(banner).index("Server:")
    #                     bg = str(banner)[starting:]
    #                     ending = bg.index("\r\n")
    #                     bg = bg[:ending]
    #                     print(bg)
    #                     bg = 'Web ' + bg 
    #                     flag = 1
    #             if flag == 0:
    #                 bg = 'Web Server : - '
                    
    #             my_canvas.drawString(80, position - 20, bg)


        
    #     # position = position + 40
        
    #     # my_canvas.drawString (45,position ,"Grabbed Banners:")
    #     # position = position + 20
        
    #     my_canvas.save()



        
        