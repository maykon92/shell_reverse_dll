import socket

def network_scan(target):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target, 80))
        return f"Porta 80 aberta em {target}"
    except Exception as e:
        return str(e)