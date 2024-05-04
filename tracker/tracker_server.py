import socket
import threading
import bencodepy # type: ignore
import time
# import pandas as pd

class TrackerServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = None
        self.clients = []
        self.torrents = {}
        self.send_lock = threading.Lock()
        self.data_check = False

    def start(self):
        # Create a socket object
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to a specific address and port
        server_address = (self.host, self.port)
        self.server_socket.bind(server_address)

        # Listen for incoming connections
        self.server_socket.listen(5)
        print('Server is listening on {}:{}'.format(*server_address))

        # Start the client checking thread
        check_thread = threading.Thread(target=self.check_clients)
        check_thread.start()

        # update_thread = threading.Thread(target=self.update_xlsx)
        # update_thread.start()

        while True:
            # Accept a client connection
            client_socket, client_address = self.server_socket.accept()
            self.clients.append(client_socket)
            #DEBUG
            # print(self.clients)
            #
            # print('New connection from {}:{}'.format(*client_address))

            # Create a new thread to handle the client
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
            client_thread.start()

    def check_clients(self):
        while True:
            time.sleep(5)
            print('------------------------------------------')
            print('Debug(clients) : ', self.clients)
            print('------------------------------------------')
            print('Debug(torrents): ', self.torrents)
            print('------------------------------------------')
            # print(self.torrents)
            for client in self.clients:
                source_host, source_port = client.getpeername()
                # print(source_host)
                # print(source_port)
                try:
                    check_message = {
                        "TOPIC": "TORRENT",
                        "HEADER": {
                            "event": "",
                            "status": "505",
                            "source_host": source_host,
                            "source_port": source_port,
                        },
                        "BODY": {}
                    }
                    encoded_check = bencodepy.encode(check_message)

                    with self.send_lock:
                        client.send(encoded_check)

                    count = 3
                    while count > 0:
                        time.sleep(1)
                        count -= 1
                        if self.data_check == True:
                            print('Client is alive')
                            break
                    if count == 0: # Client did not respond
                        print('Client is not responding')
                        self.clients = [client for client in self.clients if ((client.getpeername()[0] != source_host) and (client.getpeername()[1] != source_port))]
                        for info_hash, peers in self.torrents.items():
                            self.torrents[info_hash] = [peer for peer in peers if peer['seeder_host'] != source_host]
                        client.close()
                    self.data_check = False
                except OSError:  # Socket is closed
                    print("Client has disconnected")
                    self.clients.remove(client)
                    continue
                # Here you can perform additional checks or operations on the client if needed


    # def update_xlsx(self):
    #     #TODO write info of self.clients to xlsx file
    #     # df = pd.DataFrame(self.clients, columns=['Client Socket'])
    #     # df.to_excel('clients.xlsx', index=False)
    #     while True:
    #         time.sleep(5)
    #         # print("HAHAHA", self.clients)
    #         df = pd.DataFrame(self.clients, columns=['Client Socket'])
    #         df.to_excel('clients.xlsx', index=False)
    #         data = []
    #         for info_hash, peers in self.torrents.items():
    #             for peer in peers:
    #                 data.append([info_hash, peer['peer_id'], peer['ip'], peer['port']])
    #         df = pd.DataFrame(data, columns=['Info Hash', 'Peer ID', 'IP', 'Port'])
    #         df.to_excel('torrents.xlsx', index=False)

    #         # for info_hash, peers in self.torrents.items():
    #         #     print(f"Info Hash: {info_hash}")
    #         #     for peer in peers:
    #         #         print(f"    Peer ID: {peer['peer_id']}, IP: {peer['ip']}, Port: {peer['port']}")

    def is_client_connected(self, client_socket):
        return client_socket in self.clients

    def handle_client(self, client_socket, client_address):
        while True:
            try:
                # Receive data from the client
                data = client_socket.recv(1024)
                if data:
                    # Decode the data
                    request = bencodepy.decode(data)

                    header = request.get(b'HEADER')
                    body = request.get(b'BODY')
                    event = header.get(b'event').decode()

                    # print(header)
                    # print(body)
                    # print(event)
                    # print(source_host)
                    # print(source_port)
                    # print(seeder_host)
                    # print(seeder_port)

                    if event == 'INIT':

                        source_host = header.get(b'source_host').decode()
                        source_port = header.get(b'source_port')
                        seeder_host = header.get(b'seeder_host').decode()
                        seeder_port = header.get(b'seeder_port')
                        completed_list = body.get(b'completed_list')


                        for item in completed_list:
                            info_hash = item.get(b'info_hash').decode()
                            # piece_path = item.get(b'piece_path').decode()
                            # pieces = item.get(b'pieces')

                            if info_hash not in self.torrents:
                                self.torrents[info_hash] = [{
                                    'seeder_host': seeder_host,
                                    'seeder_port': seeder_port,
                                    # 'piece_path': piece_path,
                                    # 'pieces': pieces
                                }]
                            else:
                                self.torrents[info_hash].append({
                                    'seeder_host': seeder_host,
                                    'seeder_port': seeder_port,
                                    # 'piece_path': piece_path,
                                    # 'pieces': pieces
                                })
                        
                        response_message = {
                            "TOPIC": "TORRENT",
                            "HEADER": {
                                "event": "INIT_ACK",
                                "status": "100",
                                "source_host": source_host,
                                "source_port": source_port
                            },
                            "BODY": {}
                        }

                        encoded_response = bencodepy.encode(response_message)

                        with self.send_lock:
                            client_socket.send(encoded_response)
                        continue
                    if event == 'CHECK_RESPONSE':
                        self.data_check = True
                        completed_list = body.get(b'completed_list')
                        seeder_host = header.get(b'seeder_host').decode()
                        seeder_port = header.get(b'seeder_port')
                        for item in completed_list:
                            info_hash = item.get(b'info_hash').decode()
                            # piece_path = item.get(b'piece_path').decode()
                            # pieces = item.get(b'pieces')

                            if info_hash not in self.torrents:
                                self.torrents[info_hash] = [{
                                    'seeder_host': seeder_host,
                                    'seeder_port': seeder_port,
                                    # 'piece_path': piece_path,
                                    # 'pieces': pieces
                                }]
                            else:
                                if not any(torrent['seeder_host'] == seeder_host and torrent['seeder_port'] == seeder_port for torrent in self.torrents[info_hash]):
                                    self.torrents[info_hash].append({
                                        'seeder_host': seeder_host,
                                        'seeder_port': seeder_port
                                    })
                    else:
                        if event == 'STARTED':
                            print("ABC")
                            # send list of peers in this torrent
                            source_host = header.get(b'source_host').decode()
                            source_port = header.get(b'source_port')
                            seeder_host = header.get(b'seeder_host').decode()
                            seeder_port = header.get(b'seeder_port')
                            info_hash = body.get(b'info_hash').decode()


                            peers = [
                                {"peer_id": i, "ip": seeder['seeder_host'], "port": seeder['seeder_port']}
                                for i, seeder in enumerate(self.torrents[info_hash])
                            ]

                            if info_hash in self.torrents:
                                response_message = {
                                    "TOPIC": "TORRENT",
                                    "HEADER": {
                                        "event": "STARTED_ACK",
                                        "status": "200",
                                        "source_host": source_host,
                                        "source_port": source_port
                                    },
                                    "BODY": {
                                        "peers": 
                                            peers
                                    }
                                }

                                encoded_response = bencodepy.encode(response_message)

                                with self.send_lock:
                                    client_socket.send(encoded_response)
                            else:
                                response_message = {
                                    "TOPIC": "TORRENT",
                                    "HEADER": {
                                        "event": "STARTED_ACK",
                                        "status": "404",
                                        "source_host": source_host,
                                        "source_port": source_port
                                    },
                                    "BODY": {
                                        "message": "No peers found for this torrent"
                                    }
                                }

                                encoded_response = bencodepy.encode(response_message)

                                with self.send_lock:
                                    client_socket.send(encoded_response)

                        if event == 'COMPLETED':
                            seeder_host = header.get(b'seeder_host').decode()
                            seeder_port = header.get(b'seeder_port')
                            info_hash = body.get(b'info_hash').decode()

                            if info_hash not in self.torrents:
                                self.torrents[info_hash] = [{
                                    'seeder_host': seeder_host,
                                    'seeder_port': seeder_port
                                }]
                            else:
                                self.torrents[info_hash].append({
                                    'seeder_host': seeder_host,
                                    'seeder_port': seeder_port
                                })

                        if event == 'STOPPED':
                            source_host = header.get(b'source_host').decode()                          
                            self.clients = [client for client in self.clients if client.getpeername()[0] != source_host]
                            for info_hash, peers in self.torrents.items():
                                self.torrents[info_hash] = [peer for peer in peers if peer['seeder_host'] != source_host]

                            # close connection

            except Exception as e:
                print(f"Error handling client {client_address}: {e}")
                client_socket.close()
                self.clients.remove(client_socket)
                break

    def stop(self):
        if self.server_socket:
            self.server_socket.close()
            print('Server stopped.')

if __name__ == '__main__':
    server = TrackerServer('localhost', 12345)
    server.start()