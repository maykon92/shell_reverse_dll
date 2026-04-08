from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

KEY = b"0123456789abcdef0123456789abcdef"

def encrypt_data(data):
    cipher = AES.new(KEY, AES.MODE_ECB)
    padded_data = pad(data.encode(), AES.block_size)
    encrypted = cipher.encrypt(padded_data)
    return base64.b64encode(encrypted).decode()

def decrypt_data(encrypted_data):
    cipher = AES.new(KEY, AES.MODE_ECB)
    decrypted = cipher.decrypt(base64.b64decode(encrypted_data))
    return unpad(decrypted, AES.block_size).decode()