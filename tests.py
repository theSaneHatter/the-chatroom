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
import lib as lib

with open(os.path.expanduser('~/Desktop/Keys/school-website/public.key'), 'rb') as f:
    data = f.read()
    print(f'Key length: {len(data)} bytes')
def list_files_only(path):
    return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

# Expand user (~) and load the public key
key_path = os.path.expanduser('~/Desktop/Keys/school-website/public.key')
public_key = lib.load_public_key(key_path)
pkey_path = os.path.expanduser('~/Desktop/Keys/school-website/private.key')
private_key = lib.load_private_key(pkey_path)
# Encrypt each file in ./logs
for file in list_files_only('./logs/saves'):
    file_path = os.path.join('./logs/saves', file)
    lib.encrypt_file_line_by_line(public_key, file_path)
# decrypt each file in ./logs
#for file in list_files_only('./logs'):
#   file_path = os.path.join('./logs', file)
#   lib.decrypt_file_line_by_line(private_key, file_path)
