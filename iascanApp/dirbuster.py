import pyfiglet
from pathlib import Path
from termcolor import colored
import requests

class DirBusterDjango:
    def __init__(self):
        self.returnedDirs = []

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
        
        print("[+] Program will return to main menu once bruteforcing is complete")
        print("[+] Output will be saved in (" + djangoIP + ")_output.txt")
        print('[+] Bruteforcing Started')

        # Check domain name pattern matches
        names = []
        # Converting the file in to list of lines
        paths = []
        with open('static/wordlist_db.txt', 'r+') as f:
            for line in f:
                line = line.strip()
                if len(line) == 0:
                    continue
                else:
                    paths.append(line)   

        url_list = []    # list of all valid urls
        valid_url = 0    # total number of valid urls found

        # Check if url is valid using requests

        with Path("static/dirb_outputs/(" + djangoIP + ")_output.txt").open('w+') as out_file:
            try:
                for path in paths:

                    url = f'{url_prefix}{djangoIP}/{path}'

                    try:
                        # Sending get request to url
                        response = requests.get(url)
                        
                        # if valid print url
                        if response.status_code == 200:
                            print(colored(f'[+] {url}', 'blue'))

                            # add result to list
                            url_list.append(url)
                            self.returnedDirs.append(url)

                            # add url to output file
                            out_file.write(url+'\n')

                            valid_url += 1
                    except requests.ConnectionError:
                        pass
            except KeyboardInterrupt:
                return print("You pressed Ctrl+C")

        return url_list
        

