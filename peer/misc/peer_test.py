import threading
import json
from peer_test_define import *
import socket
import bencodepy
import queue
import hashlib
import os
from urllib.parse import urlparse
# import requests


class Peer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.peer_id = 0
        self.completed_list = []
        self.uncompleted_list = []
        self.security_code = 0
        self.client_socket = None
        self.tracker_address = ()
        self.tracker_response_queue = queue.Queue()
        self.tracker_request_lock = 0       # Lock sending message to tracker (1-lock & 0-unlock)
        self.user_command_queue = queue.Queue()

    ########################## Misc method (start) ##########################################
    def load_param(self, json_path):
        with open(json_path, "r") as file:
            torrent_list = json.load(file)
        self.security_code = torrent_list["security_code"]
        self.tracker_address = (torrent_list["tracker_ip"], torrent_list["tracker_port"])
        self.completed_list = torrent_list["completed"]
        self.uncompleted_list = torrent_list["uncompleted"]

    def user_login(self):
        # User login
        peer_username = input("Username: ")
        peer_password = input("Password: ")
        # Hash login information
        security_code = peer_username + peer_password
        # Username: admin
        # Password: 1
        while security_code != self.security_code:
            print("Wrong username or password. Please try again")

    def hash_file_name(self, file_name):
        file_name_bytes = file_name.encode('utf-8')
        hashed_bytes = hashlib.sha256(file_name_bytes)
        hashed_string = hashed_bytes.hexdigest()
        return hashed_string

    def get_metainfo(self, torrent_path):
        if os.path.exists(torrent_path):
            # Read the JSON file
            with open(torrent_path, 'r') as file:
                metainfo_dict = json.load(file)
        else:
            print("Error: The path of torrent file is not exist")
            return {}
        return metainfo_dict

    def metainfo_verification(self, metainfo_dict):
        info_hash_key = 'info_hash'
        pieces_num_key = 'pieces'
        if not isinstance(metainfo_dict, dict):
            print(f"Error: The torrent file is invalid.")
            return False
        if info_hash_key not in metainfo_dict:
            print(f"Error: The torrent file is invalid.")
            return False

    ########################## Misc method (end) ##########################################

    ########################## Handling method (start) ##########################################
    def sender_handle(self):
        # TODO
        return

    def upload_handle(self, file_path):
        # Description: Hàm sẽ xử lý việc tách file thành các pieces và lưu vào folder tương ứng, sau đó cập nhật file vào completed_list
        # Param: file_path: đường dẫn tới file cần upload
        # DuongDo:  -> Copy file trên vào folder pieces_folder
        #           -> Tạo 1 folder có định dạng tên là <file_name>_<file_exten> (vd: adc.pdf -> folder tên là 'abc_pdf')
        #           -> Tách file đó vào bên trong folder trên
        #           -> Tạo ra 1 mã info_hash từ tên file (info_hash = self.hash_file_name(<file_name>))
        #           -> Tạo 1 metainfo_dictionary gồm thông tin (info_hash, pieces_path và pieces) và thêm vào self.completed_list (Nhìn định daạng trong file TorrentList.json để hiểu rõ thêm)
        #           metainfo_dictionary = {
        #               "info_hash": "ase231r3r13",
        #               "pieces_path": "pieces_folder/abc_pdf",
        #               "pieces": 36
        #           }
        #           -> Tạo mới 1 file `.json` có tên là `<file_name>_metainfo.json` vào trong folder metainfo_folder
        #           -> Lưu dictionary của bước trên vào file '.json' đó (có thể hiểu đây là file .torrent của nhóm mình)
        # Ví dụ về các tham số
        #                   self.upload_handle('\\hehe_folder\\myCV.pdf')
        #
        # Ví dụ về định dạng tách:
        #       -> Tách nó ra 1 folder gồm các piece (giả sử dc 100 mảnh)
        #           folder name:    myCV_pdf            -> Định dạng: <file_name>_<type>
        #           folder_path     /pieces_folder/     -> Nằm trong folder pieces_folder
        #           piece name:     myCV_pdf_0.bin      -> Định dạng: <folder_name>_<piece_num>.bin
        #                           myCV_pdf_1.bin
        #                           myCV_pdf_2.bin
        #                           .............
        #                           myCV_pdf_99.bin
        return

    def download_handle(self, torrent_path):
        # Description:  Người dùng cung cấp đường dẫn đến file torrent (torrent_path) tương ứng với file cần tải
        # Todo:         -> Lấy info_hash và pieces từ file torrent (file .json)
        #               -> Gửi yêu cầu lên tracker server kèm theo info_hash + 'event' == 'started'
        #               -> Nhận peers_list từ Tracker server
        #               -> Tạo 1 bảng (pieces_state_table) về tiến trình của tất cả các piece của file cần tải
        #               |    Piece Number   |       State           |
        #               |       Piece 1     |       completed       |
        #               |       Piece 2     |       processing      |
        #               |       Piece 3     |       pending         |
        #               | ..............    |   ................    |
        #               -> pieces_state_table = ['pending'] * pieces (pieces: số lượng piece của file)
        #               -> Cập nhật info_hash + remain_pieces (remain_pieces = [index for index, element in enumerate(pieces_state_table) if element != 'completed'])
        #               -> Lần lượt tạo thread (sender_handle(self, update_pieces_state_table() )) và yêu cầu nhận piece từ các seeder khác (số thread tối đa == len(peers_list)). Và đưa các pieces state về processing
        #               ................... (Còn) ........................
        #               ************* Ngoài lề (không trong method download_handle()) ********************
        #               -> Method sender_handle() sẽ gọi hàm update_pieces_state_talble() khi kết thúc việc nhận 1 piece
        #               -> Method update_pieces_state_table(self, pass variable by reference into this method):
        #                           + Lock nhiều thread truy cập while(lock == 1): conitnue; (Tạo 1 lock cho hàm update_pieces_state_table() ở self....._lock = 0)
        #                           + Sẽ cập nhật trạng thái của pieces tiếp theo và cấp phát 1 piece mới cho thread hiện tại
        #               ********************************************************************************
        #               -> Liên tục cập nhật mảng remain_pieces
        #               -> Trong hàm download_handle() sẽ liên tục check `remain_pieces` để -> while(remain_pieces is not empty): continue (chờ đến khi các pieces đã trong trạng thái completed);
        #               -> Gửi event 'completed' đến tracker báo hiệu đã hoàn tất việc download
        ##############################################################################

        # Get metainfo from torrent file
        metainfo_dict = self.get_metainfo(torrent_path)
        # Verify the torrent file
        if self.metainfo_verification(metainfo_dict=metainfo_dict):
            return
        info_hash = metainfo_dict['info_hash']
        piece_num = metainfo_dict['pieces']

        # Send a downloading request to the tracker



    def handle_user_command(self, user_command):
        # Parse the user command
        command_split = user_command.split(':')
        command_type = command_split[0]
        command_param = command_split[1]
        if command_type == 'Download':
            self.download_handle(command_param)
        elif command_type == 'Upload':
            self.upload_handle(command_param)
        else:
            print("Error: Wrong command format")
        # if type of the command is Uploading
        #       upload_handle():
        #       -> Copy file vào pieces_folder
        #       -> Chia file vào folder phù hợp (vd: myCV.pdf -> đưa vào folder myCV_pdf trong folder pieces_folder)
        # if type of the command is Downloading
        #       download_handle():
        #       -> Chia file

        return
    ########################## Handling method (end) ##########################################

    ######################## Protocol method (start) ######################################
    def connect_to_tracker(self, tracker_address):
        # Connect to the tracker server
        self.client_socket.connect(tracker_address)

    def send_request_tracker(self, info_hash, peer_id, event, completed_torrent):
        # Wait until sender is released
        while self.tracker_request_lock == 1:
            continue
        # Lock sending message
        self.tracker_request_lock = 0
        # Send a request to the tracker
        request = bencodepy.encode({'info_hash': info_hash, 'peer_id': peer_id, 'event': event, 'completed_torrent': completed_torrent})
        self.client_socket.send(request)
        # Unlock sending message to tracker
        self.tracker_request_lock = 1

    def receive_response_tracker(self):
        # Receive the response from the tracker
        response = self.client_socket.recv(1024)
        # response_dict = bencodepy.decode(response)
        response_dict = bencodepy.decode(response)
        return response_dict

    def handle_response_tracker(self, response_dict):
        # Parse the response
        status_field = response_dict['status']
        if status_field == '200':
            print("Login successfully")
            return 1  # TODO: Handle information
        elif status_field == '404':  # Wrong information of metainfo file
            print(response_dict['message'])
            return 0
        elif status_field == '100':  # Wrong username or password
            print("Connected")
            return 1

    def handle_keep_alive_tracker(self):
        self.send_request_tracker(info_hash='', peer_id=self.peer_id, event='check_response', completed_torrent=self.completed_list)
    ######################## Protocol method (end) ######################################

    ######################## Thread method (start) ######################################
    # Description: Maintain connection with the tracker
    # def maintain_connection(self):
    #
    #     # Close: Máy bạn duy trì kết nối với tracker -> Cập nhật completed_list thường xuyên (vì người dùng có thể đưa thêm 1 file torrent mới lên hệ thống)
    #     # Description:  - Interval = 1 second
    #     #               - Message = {'event': 'check_response'}
    #
    #     return
    #
    # def user_download_check(self):
    #     # Close: Người dùng muốn tải một file trong các file torrent mà tracker đã cập nhật (nhớ kiểm tra xem file đó có trong self.file_list chưa)
    #     return
    # def user_upload_check(self):
    #     # -> Người dùng tạo 1 file torrent - "\TorrentList\abc.txt"
    #     # -> Tách nó ra 1 folder gồm casc piece (giả sử dc 100 mảnh)
    #     #       folder name:    abc_txt             <file_name>_<type>
    #     #       piece name:     abc_txt_0.bin       <folder_name>_<piece_num>.bin
    #     #                       abc_txt_1.bin
    #     #                       abc_txt_2.bin
    #     # -> Đưa vô completed_list
    #     # Close: Người dùng tạo mới 1 file torrent từ 1 file sẵn có trong máy, sau đó cập nhật file torrent đó vào Metainfo file và self.file_list (Việc cập nhật lên server sẽ ằm ở thread maintain_connection)
    #     return

    def tracker_check(self):
        while True:
            message = self.receive_response_tracker()
            # Handle immediately (if message is a keep-alive message)
            if 'status' in message:
                if message['status'] == '505':
                    self.handle_keep_alive_tracker()
                    return
            self.tracker_response_queue.put(message)

    def user_check(self):
        while True:
            user_command = input("User command-line: ")
            self.user_command_queue.put(user_command)

    def user_handle(self):
        while True:
            if self.user_command_queue.qsize() > 0:
                # Todo: Handle user command ()
                self.handle_user_command(self.user_command_queue.get())

    def leecher_check(self):
        leecher_handle = socket.socket()
        leecher_handle.bind(('localhost', 5003))
        leecher_handle.listen(5)

        while True:
            # Tạo 1 thread khi có 1 leecher kết nối đến và thread đó handle phần giao tiếp
            break
        # Handshake (receiver -> sender)
        packet = {
            "TOPIC": "DOWNLOAD REQUEST",
            "HEADER": {
                'type': 'Handshake',
                'source_ip': "1:1:1:1",
                'source_port': 5003,
                'info_hash': 'fdjasodfjoewi0f'
            }
        }
        # Handshake (sender -> receiver)
        # Nếu sender có file đó (check 'info_hash' xem có ko)
        packet = {
            "TOPIC": "UPLOADING",
            "HEADER": {
                'type': 'ACK',
                'source_ip': "1:1:1:1",
                'source_port': 5000,
                'info_hash': '123'
            }
        }
        # Nếu sender ko có file đó
        packet = {
            "TOPIC": "UPLOADING",
            "HEADER": {
                'type': 'NACK',
                'source_ip': "1:1:1:1",
                'source_port': 5000,
                'info_hash': '123'
            }
        }
        # Todo: assign to Sy Duong
        # Todo: Một peer khác kết nối với đến máy bạn để tải file từ máy bạn.
        return

    ######################### Thread method (end) #######################################

    ######################### Flow method (start) #######################################
    def establish_connection(self):
        info_hash = ''
        print("Connecting to the tracker ......")
        while True:
            self.send_request_tracker(info_hash, self.peer_id, 'init', self.completed_list)
            response = self.receive_response_tracker()
            if self.handle_response_tracker(response) == 1:
                break

    def start(self):
        # Load the previous param of the peer
        self.load_param("../TorrentList.json")

        # User login
        self.user_login()

        # Create a socket
        self.client_socket = socket.socket()

        # Bind the socket to address and port
        self.client_socket.bind((self.host, self.port))

        # Establish connection (Transport layer handshake)
        self.connect_to_tracker(self.tracker_address)

        # Establish connection (Application layer Handshake): The peer send metainfo to the tracker
        self.establish_connection()

        # Create 3 main threads -> leecher_check (another peer want to download your file)
        #                       -> tracker_check: receive message from the tracker and store the message to stack
        #                       -> user_check: receive user's command
        #                       (delete) -> maintain_connection (keep-alive and updating metainfo message with the tracker)
        #                       (delete) -> user_download_check: user want to download a new file  -> "start downloading" stage
        #                       (delete) -> user_upload_check: user want to upload a new torrent file to tracker
        leecher_check_thread = threading.Thread(target=self.leecher_check())
        leecher_check_thread.start()

        tracker_check_thread = threading.Thread(target=self.tracker_check())
        tracker_check_thread.start()

        user_check_thread = threading.Thread(target=self.user_check())
        user_check_thread.start()

    ######################### Flow method (end) #######################################


if __name__ == '__main__':
    peer = Peer('localhost', 5002)
    peer.start()