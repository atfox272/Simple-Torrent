import requests
import bencodepy
import hashlib
import os


"""
name: parse_metainfo
input: metainfo_file: str - the path to the .torrent file
output: metainfo: dict - the parsed metainfo file
action: use bencodepy to decode the metainfo file
"""
def parse_metainfo(metainfo_file):
    with open(metainfo_file, 'rb') as f:
        metainfo = bencodepy.decode(f.read())
    return metainfo


"""
name: request_tracker
input: tracker_url: str - the URL of the tracker
       info_hash: bytes - the info hash of the torrent
       peer_id: bytes - the peer ID
output: response: requests.Response - the response from the tracker
action:send a request to the tracker with the info hash and peer ID as parameters
"""
def request_tracker(tracker_url, info_hash, peer_id, port=6881):
    params = {
        'info_hash': info_hash,
        'peer_id': peer_id,
        'compact': 1,
        'port': port,
        # Add other required parameters here
    }
    response = requests.get(tracker_url, params=params)
    return response


"""
name: parse_peers
input: response: requests.Response - the response from the tracker
output: parsed_peers: list - a list of dictionaries containing the IP address and port of the peers
action: parse the response from the tracker to extract the IP address and port of the peers
"""
def parse_peers(response):
    peers = bencodepy.decode(response.content)[b'peers']
    parsed_peers = []
    for i in range(0, len(peers), 6):
        ip = '.'.join(str(peers[i + j]) for j in range(4))
        port = (peers[i + 4] << 8) + peers[i + 5]
        parsed_peers.append({'ip': ip, 'port': port})
    return parsed_peers


"""
name: get_tracker_url
input: metainfo: dict - the parsed metainfo file
output: tracker_url: str - the URL of the tracker
action: extract the tracker URL from the metainfo file
"""
def get_tracker_url(metainfo):
    tracker_url = metainfo[b'announce'].decode()
    return tracker_url


"""
name: get_info_hash
input: metainfo: dict - the parsed metainfo file
output: info_hash: bytes - the info hash of the torrent
action: calculate the SHA-1 hash of the 'info' key in the metainfo file
"""
def get_info_hash(metainfo):
    info = bencodepy.encode(metainfo[b'info'])
    info_hash = hashlib.sha1(info).digest()
    return info_hash


"""
name: generate_peer_id
output: peer_id: bytes - a randomly generated peer ID
action: generate a 20-byte peer ID using os.urandom
"""
def generate_peer_id():
    return os.urandom(20)


"""
name: get_piece_length
input: metainfo: dict - the parsed metainfo file
output: piece_length: int - the length of each piece in bytes
action: extract the piece length from the metainfo file
"""
def get_piece_length(metainfo):
    piece_length = metainfo[b'info'][b'piece length']
    return piece_length


"""
name: get_piece_count
input: metainfo: dict - the parsed metainfo file
output: piece_count: int - the number of pieces in the torrent
action: calculate the number of pieces by dividing the total length of the pieces by 20
"""
def get_piece_count(metainfo):
    pieces = metainfo[b'info'][b'pieces']
    return len(pieces) // 20


"""
name: get_pieces
input: metainfo: dict - the parsed metainfo file
output: pieces: list - a list of 20-byte strings representing the pieces
action: split the 'pieces' key in the metainfo file into 20-byte strings
"""
def get_pieces(metainfo):
    pieces = metainfo[b'info'][b'pieces']
    return [pieces[i:i+20] for i in range(0, len(pieces), 20)]


"""
name: parse_files
input: metainfo: dict - the parsed metainfo file
output: files: list - a list of dictionaries containing the length and path of each file
action: parse the 'files' key in the metainfo file to extract the length and path of each file
"""
def parse_files(metainfo):
    info = metainfo[b'info']
    if b'files' in info:
        # Multiple files
        files = [{'length': f[b'length'], 'path': '/'.join([part.decode() for part in f[b'path']])} for f in info[b'files']]
    else:
        # Single file
        files = [{'length': info[b'length'], 'path': info[b'name'].decode()}]
    return files


"""
name: map_pieces_to_files
input: files: list - a list of dictionaries containing the length and path of each file
       piece_length: int - the length of each piece
output: piece_map: list - a list of dictionaries containing the piece index, file index, and file offset of each piece
action: map the piece address space to the file address space
"""
def map_pieces_to_files(files, piece_length):
    piece_map = []
    piece_index = 0
    for file_index, file in enumerate(files):
        file_offset = 0
        while file_offset < file['length']:
            piece_map.append({'piece_index': piece_index, 'file_index': file_index, 'file_offset': file_offset})
            piece_index += 1
            file_offset += piece_length
    return piece_map


# Example usage
metainfo_file = 'C:/Users/datph/Downloads/05-star.-wars.-4-k-77.1080p.no-dnr.-35mm.x-264-v-1.0-et-hd_archive.torrent'
metainfo = parse_metainfo(metainfo_file)
tracker_url = get_tracker_url(metainfo)
info_hash = get_info_hash(metainfo)
peer_id = generate_peer_id()
piece_length = get_piece_length(metainfo)
piece_count = get_piece_count(metainfo)
pieces = get_pieces(metainfo)
response = request_tracker(tracker_url, info_hash, peer_id)
parsed_peers = parse_peers(response)
files = parse_files(metainfo)
piece_map = map_pieces_to_files(files, piece_length)




# Take ip and port from parsed_peers
for peer in parsed_peers:
    print(peer)



























# Debug
# print(metainfo)
# print(piece_length)
# print(tracker_url)
# print(info_hash)
# print(peer_id)
# pieces = get_pieces(metainfo)
# print(pieces)
# for i, piece in enumerate(pieces):
#     print(f"Piece {i}: {piece}")
#
# print(response.content)
# for peer in parsed_peers:
#     print(peer)
# for file in files:
#     print(f"Path: {file['path']}, Length: {file['length']}")
# for piece in piece_map[:10]:
#     print(f"Piece Index: {piece['piece_index']}, File Index: {piece['file_index']}, File Offset: {piece['file_offset']}")