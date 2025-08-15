#!/usr/bin/env python3

import time
import math
from datetime import datetime
import subprocess as subp
import numpy as np

def get_time():
    now = datetime.now()
    time_string = now.strftime("%H:%M:%S")
    return time_string



def log(message, logfile='./logs/logs.txt', ip='0.0.0.0'):
    now = datetime.now()
    timestamp = now.strftime('%d/%m/%y') +','+ get_time()
    with open(logfile, 'a') as file:
        file.write(f'{timestamp}[{ip}]:>{message}<\n')
    file.close()
    return True

def backup_logs(logfile='./logs/logs.txt', savefile='./logs/saves'):
    now = datetime.now()
    timestamp = now.strftime('%d-%m-%y') +'.'+ get_time()
    subp.run(['cp',logfile,f'{savefile}/{timestamp}.txt'])
    return True


def gen_usrname(ip):
    last3 = str(ip).split('.')[3]
    usrname = str(last3)
    usrnameType = 'letters'
    if usrnameType == 'letters':
        last3 = list(last3)
        last3 = np.array(last3, dtype=int)
        letters = 'abcdefghijklmnopqrstuvwxyz'
        letters = np.array(list(letters))
        usrname = list(letters[last3])
        usrname = ''.join(usrname)
        print(f'Genorated username')

    return usrname

def gen_prefix(ip):
    usrname = gen_usrname(ip)
    time_format = "%H:%M:%S"
    prefix = {'usrname':usrname, 'time_format':time_format}

    return prefix
