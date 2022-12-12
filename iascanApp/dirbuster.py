import pyfiglet
from pathlib import Path
import requests

class DirBusterDjango:
    def __init__(self):
        self.returnedDirs = [] # çıktı sonucu bulunan dizinler.

    def backendTerminal(self,djangoIP,djangoSSL):
        print("************************************************\n")
        ascii_banner= pyfiglet.figlet_format("       iascan backend         dirbuster")
        print(ascii_banner)
        print("************************************************")
                
        """
            DIR BUSTER
        """

        if djangoSSL == "SSL Enabled":
            url_prefix = "https://"
        else:
            url_prefix = "http://"
        names = []
        paths = []
        with open('static/wordlist_db.txt', 'r+') as f:
            for line in f:
                line = line.strip()
                if len(line) == 0:
                    continue
                else:
                    paths.append(line)   

        url_list = []    # geçerli urller
        valid_url = 0    # geçerli url sayısı
        try:
            for path in paths:

                url = f'{url_prefix}{djangoIP}/{path}'

                try:
                    # siteye get requesti gönder
                    response = requests.get(url)
                    
                    # eğer siteden http:200  mesajı dönerse (yani dizin aktifse)
                    if response.status_code == 200:
                        print(f'[+] {url}')

                        # sonucu listeye ekle
                        url_list.append(url)
                        self.returnedDirs.append(url)
                        valid_url += 1
                except requests.ConnectionError:
                    pass
        except KeyboardInterrupt:
            return print("Keyboard Interrupt -> Ctrl+C")
        return url_list
    

