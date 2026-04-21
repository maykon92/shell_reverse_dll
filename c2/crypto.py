# c2/crypto.py - Gerenciamento de criptografia

import os
import base64
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad, unpad
import secrets

class CryptoManager:
    def __init__(self):
        self.rsa_private_key = None
        self.rsa_public_key = None
        self.key_files_exist = False
        
    def generate_rsa_keys(self):
        """Gera par de chaves RSA 2048 bits"""
        self.rsa_private_key = RSA.generate(2048)
        self.rsa_public_key = self.rsa_private_key.publickey()
        
        # Salva em arquivos para persistência
        with open('c2_private.pem', 'wb') as f:
            f.write(self.rsa_private_key.export_key('PEM'))
        
        with open('c2_public.pem', 'wb') as f:
            f.write(self.rsa_public_key.export_key('PEM'))
        
        self.key_files_exist = True
        return True
    
    def load_rsa_keys(self):
        """Carrega chaves existentes"""
        try:
            with open('c2_private.pem', 'rb') as f:
                self.rsa_private_key = RSA.import_key(f.read())
            
            with open('c2_public.pem', 'rb') as f:
                self.rsa_public_key = RSA.import_key(f.read())
            
            self.key_files_exist = True
            return True
        except:
            return False
    
    def get_public_key_pem(self):
        """Retorna chave pública em formato PEM"""
        if not self.rsa_public_key:
            self.load_rsa_keys() or self.generate_rsa_keys()
        return self.rsa_public_key.export_key('PEM').decode()
    
    def decrypt_session_key(self, encrypted_key_b64):
        """Descriptografa chave de sessão AES com RSA privada"""
        if not self.rsa_private_key:
            self.load_rsa_keys()
        
        encrypted_key = base64.b64decode(encrypted_key_b64)
        cipher_rsa = PKCS1_OAEP.new(self.rsa_private_key)
        session_key = cipher_rsa.decrypt(encrypted_key)
        return session_key
    
    def encrypt_aes(self, data, key):
        """Criptografa com AES-256-CBC"""
        iv = secrets.token_bytes(16)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        encrypted = cipher.encrypt(pad(data.encode(), AES.block_size))
        return base64.b64encode(iv + encrypted).decode()
    
    def decrypt_aes(self, encrypted_b64, key):
        """Descriptografa com AES-256-CBC"""
        data = base64.b64decode(encrypted_b64)
        iv = data[:16]
        encrypted = data[16:]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = unpad(cipher.decrypt(encrypted), AES.block_size)
        return decrypted.decode()