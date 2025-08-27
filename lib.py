#!/usr/bin/env python3
print(f'{__name__} has been imported')
import time
import math
from datetime import datetime
import subprocess as subp
import numpy as np
import json
import os
import cryptography
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import base64
import nacl.utils
import nacl.secret
from nacl.public import PrivateKey, SealedBox, PublicKey

def get_time():
    now = datetime.now()
    time_string = now.strftime("%H-%M-%S")
    return time_string


def log(message, logfile='./logs/logs.txt', ip='0.0.0.0', encrypt=False, public_key=None):
    now = datetime.now()
    timestamp = now.strftime('%d/%m/%y') +','+ get_time()
    log_msg = f'{timestamp}[{ip}]:>{message}<\n'
    if encrypt:
        if public_key==None:
            print(f'\033[31m@error:log(): encryption wanted, but no public key given')
        print(f'@lib:log():appending encrypted message:>{log_msg}<')
        append_encrypted_message(public_key, logfile, log_msg)

    else:
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

#still need complete
def forword_to_all(foword_fn,path=os.path.join(os.getcwd())):
    data = load_json(path=path)
    #for i in data['nodes']:

def fix_old_log_formating(path):
    for file in os.listdir(path):
        new_name = file.replace(':', '-')
        os.rename(os.path.join(path, file), os.path.join(path, new_name))
# encryption of logs :
'''
To gen asymmetric key pair etc:
private_key = PrivateKey.generate()
public_key = private_key.public_key
box = SealedBox(public_key)
'''

def encrypt(public_key,data):
    box = SealedBox(public_key)
    if type(data) != bytes:
        print(f'\033[33mWorning from encrypt(): data is not of type bytes. type:>{type(data)}<\033[0m')
        data = bytes(data, 'utf-8')
    encrypted = box.encrypt(data)
    return encrypted

def decrypt(private_key, data):
    if type(data) != bytes:
        print(f'\033[33mWorning from encrypt(): data is not of type bytes. type:>{type(data)}<')
        data = bytes(data, 'utf-8')
    box = SealedBox(private_key)
    decrypted = box.decrypt(data)
    return decrypted

def load_private_key(private_key_path):
    with open(private_key_path, 'rb') as file:
        private_key = PrivateKey(file.read())
    return private_key

def load_public_key(public_key_path):
    with open(public_key_path, 'rb') as file:
        public_key = PublicKey(file.read())
    return public_key

def save_key(file_path, keytes):
    if type(key) != bytes:
        key = bytes(str(key),'utf-8')
    with open(file_path, 'wb') as file:
        file.write(key)
    return True

def encrypt_file_line_by_line(public_key, file_path):
    encrypted_lines = []
    with open(file_path, 'rb') as file:
        for line in file:
            encrypted_line = encrypt(public_key, line)
            encrypted_lines.append(encrypted_line)

    with open(file_path, 'wb') as file:
        for line in encrypted_lines:
            line_len = len(line)
            file.write(line_len.to_bytes(4, 'big'))  #write 4-byte length prefix
            file.write(line)

def decrypt_file_line_by_line(private_key, file_path):
    decrypted_lines = []
    with open(file_path, 'rb') as file:
        while True:
            len_bytes = file.read(4)  #read 4-byte length prefix
            if not len_bytes:
                break
            line_len = int.from_bytes(len_bytes, 'big')
            encrypted_line = file.read(line_len)
            decrypted_line = decrypt(private_key, encrypted_line)
            decrypted_lines.append(decrypted_line)

    with open(file_path, 'wb') as file:
        for line in decrypted_lines:
            file.write(line)

def append_message(file_path, message):
    if type(message) != bytes:
        message = bytes(message,'utf-8')

    length = len(message)
    with open(file_path, 'ab') as f:
        f.write(length.to_bytes(4, 'big'))  # 4 bytes so 2**32 max size
        f.write(message)

def append_encrypted_message(public_key, file_path, message):
    if type(message) != bytes:
        message = bytes(message,'utf-8')
    encrypted = encrypt(public_key, message)
    print(f'@lib:append_encrypted_message():appending enctypted message to {file_path}, encrypted message:>{encrypted}<')
    append_message(file_path, encrypted)

