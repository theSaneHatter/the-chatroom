#!/usr/bin/env python3

import cryptography
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
import sys
import os

if len(sys.argv) != 3:
    print("error: specify key and file")
    print('syntax: file, key')
    exit(-1)

targ_file_path = sys.argv[1]
with open(targ_file_path, 'rb') as og_file:
    og_data = og_file.read()

pub_pem_path = sys.argv[2]
with open(pub_pem_path, 'rb') as pub_key_file:
     public_key = serialization.load_pem_public_key(
        pub_key_file.read()
    )


encrypted = public_key.encrypt(
    og_data,
    padding.OAEP(
        mgf = padding.MGF1(algorithm=hashes.SHA256()),
        algorithm = hashes.SHA256(),
        label=None
    )
)

with open(targ_file_path+'.incripted', 'wb') as encrypted_file:
    encrypted_file.write(encrypted)
print('soccess')
