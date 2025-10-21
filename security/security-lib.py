#!/usr/bin/env python3


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
