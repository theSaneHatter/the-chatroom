#!/usr/bin/env python3

import time
import math
from datetime import datetime
import subprocess as subp
import numpy as np
import json
import os

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


def gen_username(ip):
    last3 = str(ip).split('.')[3]
    username = str(last3)
    zeros = '000'
    required_zeros = 3 - len(username)
    username = ''.join(str(zeros[:required_zeros])) + username
    usernametype = 'not-letters'
    if usernametype == 'letters':
        last3 = list(last3)
        last3 = np.array(last3, dtype=int)
        letters = 'abcdefghijklmnopqrstuvwxyz'
        letters = np.array(list(letters))
        username = list(letters[last3])
        username = ''.join(username)
        print(f'genorated username')
    return username

def gen_prefix(ip):
    username = gen_username(ip)
    time_format = "%H:%M:%S"
    prefix = {'username':username, 'time_format':time_format}

    return prefix

def load_json(path=os.path.join(os.getcwd(), 'config.json')):
    with open(path,'r') as file:
        data = json.load(file)
        file.close()
    return data

def forword_to_all(foword_fn,path=os.path.join(os.getcwd())):
    data = load_json(path=path)
