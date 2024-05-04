import socket
import bencodepy

class Client:
    def __init__(self):
        # Create a socket object
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_to_tracker(self, server_address):
        # Connect to the tracker server
        self.client_socket.connect(server_address)
        print('Connected to {}:{}'.format(*server_address))

    def send_request(self, info_hash, peer_id, event):
        # Send a request to the tracker
        request = bencodepy.encode({b'info_hash': info_hash, b'peer_id': peer_id, b'event': event})
        self.client_socket.send(request)

    def receive_response(self):
        # Receive the response from the tracker
        response = self.client_socket.recv(1024)
        response_dict = bencodepy.decode(response)

        if response_dict[b'status'] == b'200':
            print('Received list of peers from tracker:', response_dict[b'peers'])
        else:
            print('Error:', response_dict[b'message'])
        if response == b'505':
            print('Received check message from server')
            # Send a response back to the server
            self.send_response(b'alive')
    def close_connection(self):
        # Close the socket connection
        self.client_socket.close()

if __name__ == '__main__':
    client = Client()
    server_address = ('localhost', 12345)
    client.connect_to_tracker(server_address)

    info_hash = b'a\t\xc6\xb4LV\x04\x8a\x83\xaeM\x06W\\\x8d:\x87{i\xeb'
    peer_id = b'\xd5\xb4\xf3\xdf\x1e){\xb0C*r\xe7\xfe\xdc\xbd\xb6J\xc0\x96\x1b'
    event = b'completed'

    client.send_request(info_hash, peer_id, event)
    try:
        while True:
            client.receive_response()
    except KeyboardInterrupt:
        client.close_connection()
    # client.close_connection()