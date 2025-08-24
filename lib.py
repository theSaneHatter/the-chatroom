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

def get_time():
    now = datetime.now()
    time_string = now.strftime("%H-%M-%S")
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

#still need complete
def forword_to_all(foword_fn,path=os.path.join(os.getcwd())):
    data = load_json(path=path)
    #for i in data['nodes']:

def encrypt(pub_key, data):
    public_key = pub_key
    if not type(data) == bytes:
        og_data = data.encode('utf-8')
    else:
        og_data = data
    encrypted = public_key.encrypt(
        og_data,
        padding.OAEP(
            mgf = padding.MGF1(algorithm=hashes.SHA256()),
            algorithm = hashes.SHA256(),
            label=None
        )
    )
    return encrypted

def encrypt_file(pub_key_path, file_path):
    with open(pub_key_path, 'rb') as pub_key_file:
        pub_key = pub_key_path.read()

    with open(file_path, 'rb') as file:
        og_data = og_file.read()
    encrypted_data = encrypt(pub_key, og_data)
    with open(file_path, 'wb') as file:
        file.write(encrypted_data)
    print(f'encrypted {file_path}')
    return True

def decrypt(private_key, data):
    if not type(data) == bytes:
        data = bytes(data, 'utf-8')
    decrypted = private_key.decrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted

def decrypt_file(private_key_path, data_path):
    with open(priv_pem_path,'rb') as priv_pem_file:
        private_key = serialization.load_pem_private_key(
            priv_pem_file.read(),
            password=None
        )

    with open(data_path, 'rb') as data_file:
        data = data_file.read()

    decrypted = decrypt(private_key, data)
    print(f'decrypted file: {decrypted}')
    return decrypted

def load_priv_key(private_key_path):
    with open(private_key_path, 'rb') as priv_pem_file:
        private_key = serialization.load_pem_private_key(
            priv_pem_file.read(),
            password=None
        )
    return private_key

def load_pub_key(public_key_path):
    with open(public_key_path, 'rb') as pub_key_file:
        public_key = serialization.load_pem_public_key(
            pub_key_file.read()
        )
    return public_key

def gen_priv_key():
    private_key = rsa.generate_private_key(
        public_exponent = 65537,
        key_size = 2048
    )
    print(f'genorated private key: {private_key}')
    return private_key

def gen_priv_pem(private_key):
    prev_pem = private_key.private_bytes(
        encoding = serialization.Encoding.PEM,
        format = serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm = serialization.NoEncryption()
    )
    print(f'genorated private pem: {prev_pem}')
    return prev_pem

def gen_pub_key(private_key):
    public_key = private_key.public_key()
    return public_key

def gen_pub_pem(public_key):
    pub_pem = public_key.public_bytes(
        encoding = serialization.Encoding.PEM,
        format = serialization.PublicFormat.SubjectPublicKeyInfo
    )
    print(f'genorated public pem: {pub_pem}')
    return pub_pem

def decrypt_lines(private_key_path, file_path):
    private_key = load_priv_key(private_key_path)
    lines = []
    with open(file_path, 'r+') as file:
        for line in file:
            print(f'encrypted line: {line}')
            decrypted = decrypt(private_key, line)
            lines.append(decrypted)
            print(f'decrypted line: decrypted')
    with open(file_path, 'w') as file:
        for line in lines:
            file.write(line)
    return True

import base64

def encrypt_lines(public_key_path, file_path):
    public_key = load_pub_key(public_key_path)
    print(f'@debug:public key:{public_key}')
    lines = []

    # Read original lines
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            encrypted = encrypt(public_key, line.strip())
            encoded = base64.b64encode(encrypted).decode('utf-8')
            lines.append(encoded)

    # Overwrite file with base64-encoded encrypted lines
    with open(file_path, 'w', encoding='utf-8') as file:
        for encoded_line in lines:
            file.write(encoded_line + '\n')
