import socket
import tqdm
import os
#from peer_proc import *


def send_file(source_host, source_port, dest_host, dest_port, file_path):
    SEPARATOR = "<SEPARATOR>"
    BUFFER_SIZE = 4096 # send 4096 bytes each time step

    # Receiver IP address
    host = dest_host

    # Receiver port
    port = dest_port

    # print('Debug(2): ', file_path)
    # the name of file we want to send
    filename = os.path.basename(file_path)  #Send all file types but, not in directory \User (causes error)

    # get the file size
    # filesize = os.path.getsize(file_path)
    filesize = 1
    # create the client socket
    s = socket.socket()

    # s.bind((source_host, source_port))

    print(f"[+] Connecting to {host}:{port}")
    while True:
        try:
            s.connect((host, port))
            break
        except:
            print('Warning: Retry to connect to 1 leecher-------------------------------')
    print("[+] Connected.")

    # send the filename and filesize
    s.send(f"{filename}{SEPARATOR}{filesize}".encode())

    # start sending the file

    with open(file_path, "rb") as f:
        while True:
            # read the bytes from the file
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                # file transmitting is done
                break
            # we use sendall to assure transmission in
            # busy networks
            # print(f'Debug(20): {bytes_read}')
            s.send(bytes_read)
    # close the socket

    s.close()
    return True

# dest_host = "192.168.150.117"    # 10.0.227.150 # ip cua may dich
# dest_port = 5000
# file_path = "input136.txt"
# source_host = "192.168.150.104" #ip cua may
# source_port = 5000
#
# a = send_file(source_host, source_port, dest_host,dest_port,file_path)