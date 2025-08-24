#!/usr/bin/env python3
import cryptography
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
import sys

if len(sys.argv) != 3:
    print("error: invalid arguements")
    print("useage: encrypted-file, private-key")
    exit(-1)


encrypted_file_path = sys.argv[1]
with open(encrypted_file_path, 'rb') as encrypted_file:
    encrypt = encrypted_file.read()

priv_pem_path = sys.argv[2]

with open(priv_pem_path,'rb') as priv_pem_file:
    private_key = serialization.load_pem_private_key(
        priv_pem_file.read(),
        password=None
    )
    decrypted = private_key.decrypt(
        encrypt, # The encrypted data goes first
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    with open(encrypted_file_path+'.decrypted', 'wb') as decrypted_file:
        decrypted_file.write(decrypted)

print(f'decrypted file: {decrypted}')
