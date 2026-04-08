import base64

OBFUSCATED_STRING = "QmFzZTY0IGVuY29kZWQgc3RyaW5n"

def decode_string():
    return base64.b64decode(OBFUSCATED_STRING).decode()