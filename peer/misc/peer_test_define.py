import socket


def find_unused_port(start_port=5003, end_port=65535):
    for port in range(start_port, end_port + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('localhost', port))
            except OSError:
                # Port is already in use
                continue
            return port
    raise Exception("Error: No unused port found in the specified range (You are using too many resources)")