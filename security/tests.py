#!/usr/bin/env python3
import time
import math
from datetime import datetime
import subprocess as subp
import numpy as np
import json
import os
import nacl.utils
import nacl.secret
from nacl.public import PrivateKey, SealedBox, PublicKey



private_key = PrivateKey.generate()
print(f'priv key:{str(private_key)}')
public_key = private_key.public_key
print(f'pub key:{public_key}')
box = SealedBox(public_key)

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

def save_key(file_path, key):
    if type(key) != bytes:
        key = bytes(key,'utf-8')
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
    append_message(file_path, encrypted)


with open('encrypt-me.txt', 'rb') as file:
    print(f'contents of encrypt-me.txt:>{file.read()}<')
encrypt_file_line_by_line(public_key, 'encrypt-me.txt')
with open('encrypt-me.txt', 'rb') as file:
    print(f'contents of encrypt-me.txt:>{file.read()}<')
append_encrypted_message(public_key, 'encrypt-me.txt', 'can you see me?')
with open('encrypt-me.txt', 'rb') as file:
    print(f'contents of encrypt-me.txt:>{file.read()}<')
decrypt_file_line_by_line(private_key, 'encrypt-me.txt')
with open('encrypt-me.txt', 'rb') as file:
    print(f'contents of encrypt-me.txt:>{file.read()}<')
