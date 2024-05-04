import socket
import tqdm
import os


class FileReceiver:
    SEPARATOR = "<SEPARATOR>"
    BUFFER_SIZE = 4096  # receive 4096 bytes each time

    def __init__(self, host, port, directory):
        self.host = host
        self.port = port
        self.directory = directory
        self.server_socket = socket.socket()  # TCP socket
        self.server_socket.bind((self.host, self.port))
        self.client_socket = None
        self.client_address = None

    def config_receiver(self, separator_in, buffer_size_in):
        self.SEPARATOR = separator_in
        self.BUFFER_SIZE = buffer_size_in

    def start(self):
        self.server_socket.listen(5)  # enable the server to accept connections
        # print(f"[*] Listening as {self.host}:{self.port}")
        self.client_socket, self.client_address = self.server_socket.accept()  # accept connection if there is any
        # print(f"[+] {self.client_address} is connected.")

    def receive_file(self):
        ########
        # self.client_socket, self.client_address = self.server_socket.accept()  # accept connection if there is any
        # print(f"[+] {self.client_address} is connected.")
        #######
        received = self.client_socket.recv(self.BUFFER_SIZE).decode()
        filename, filesize = received.split(self.SEPARATOR)
        filename = os.path.basename(filename)  # remove absolute path if there is

        # create the directory if it does not exist
        os.makedirs(self.directory, exist_ok=True)

        # add the directory path to the filename
        filename = os.path.join(self.directory, filename)

        #filesize = int(filesize)  # convert to integer

        with open(filename, "wb") as f:
            while True:
                bytes_read = self.client_socket.recv(self.BUFFER_SIZE)
                if not bytes_read:
                    break  # file transmitting is done
                f.write(bytes_read)  # write to the file the bytes we just received

    def close_connection(self):
        self.client_socket.close()
        self.server_socket.close()



# usage
# path = "E:\\OneDrive - VNU-HCMUS\\Desktop\\test"
# server = FTPReceiver('192.168.150.117', 5000, path)
# server.start()
# server.receive_file()
# server.close_connection()