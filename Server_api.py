#!/usr/bin/python3
import socket
import struct
import json
import time
import zlib
from PacketDecoder import packet


# will use when online mode is added (please add if you have free time [I don't have internet on my desktop, so I can't])
# import rsa


class Server:
    def __init__(self, host='localhost', port=25565, username='', timeout=5, quiet=True):
        # Init the hostname, port, timeout and username (username not needed yet)
        self._host = host
        self._port = port
        self._username = username
        self._timeout = timeout
        self.quiet = quiet
        self.play = False  # this should never start in True for a normal login
        self.decode_packet_login = packet["decode"]["login"]
        self.decode_packet = packet["decode"]["play"]
        self.encode_packet = packet["encode"]

    @staticmethod
    def _unpack_varint(sock):  # Unpacks a varint
        data = 0
        for i in range(5):
            ordinal = sock.recv(1)

            if len(ordinal) == 0:
                break

            byte = ord(ordinal)
            data |= (byte & 0x7F) << 7 * i

            if not byte & 0x80:
                break

        return data

    @staticmethod
    def _pack_varint(data):  # Packs a var int
        ordinal = b''

        while True:
            byte = data & 0x7F
            data >>= 7
            ordinal += struct.pack('B', byte | (0x80 if data > 0 else 0))

            if data == 0:
                break

        return ordinal

    def _pack_data(self, data):  # packs data into a packet
        if type(data) is str:
            data = data.encode('utf8')
            return self._pack_varint(len(data)) + data

        elif type(data) is int:
            return struct.pack('H', data)

        elif type(data) is float:
            return struct.pack('Q', int(data))

        elif type(data) is bool:
            return struct.pack('?', data)

        else:
            return data

    def send_data(self, connection, *args):  # Sends the packet to the server
        data = b''

        for arg in args:
            data += self._pack_data(arg)

        data = self._pack_varint(len(data)) + data

        if not self.quiet:
            print(f'out\t{data}')

        connection.send(data)

    def read_fully(self, connection, extra_varint=False, return_id=False):  # Read the connection and return the bytes
        packet_length = self._unpack_varint(connection)
        packet_id = self._unpack_varint(connection)
        if not self.quiet:
            print(f"\n{packet_length}")
            print(hex(packet_id))
        byte = b''

        if extra_varint:
            # Packet contained netty header offset for this
            if packet_id > packet_length:
                self._unpack_varint(connection)

            extra_length = self._unpack_varint(connection)

            while len(byte) < extra_length:
                byte += connection.recv(extra_length)

        else:
            byte = connection.recv(packet_length)

        if byte != b'':
            if not self.quiet:
                print(f'in\t{byte}')

        try:
            return zlib.decompress(byte)
        except:
            return byte

    def offline_login(self, version="1.18.2", quiet=True):
        if quiet != self.quiet:
            self.quiet = quiet

        if self._username == '':
            raise ValueError("Username can't be blank when logging in")

        """
        0: handshake                out     starts connection and gives connection data
        1: login start              out     gives username
        maby 2: Set Compression     in      max size before a outgoing packet must be compressed (zlib)
        maby 2: Login success       in      ADD DESCRIPTION
        3: login play               in      ADD DESCRIPTION
        4: custom payload           in      ADD DESCRIPTION
        5: ADD
        """

        # start socket, set the timeout and connect to the minecraft server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection:
            connection.settimeout(self._timeout)
            connection.connect((self._host, self._port))

            # handshake and setup login
            if version == "1.18.2":  # 1.18.2
                self.send_data(connection, b'\x00', 1526, socket.gethostname(), self._port, b'\x02')  # handshake, 1526 is 1.18.2's raw protocol number, should be able to change to 1.19.2's easily due to no packet changes (just blocks and mobs)
            elif version == "1.19.2":  # 1.19.2
                self.send_data(connection, b'\x00', 1528, socket.gethostname(), self._port, b'\x02')
            self.send_data(connection, b'\x00', self._username)  # login

            # max length before compression doesn't seem to work here

            login_suc_bytes = self.read_fully(connection)
            login_uuid, login_username, login_suc_bytes = self.decode_packet_login[0x02](login_suc_bytes)
            print(f"login success: \n\tuuid:{login_uuid}\n\tusername: {login_username}\n\textra:{login_suc_bytes}\n")  # Login success

            self.play = True  # activate play mode

            play_user_id, play_hardcore, gamemode, prevous_gamemode, num_in_next, rest_of_data = self.decode_packet[0x26](self.read_fully(connection))
            if gamemode == b'\x00':
                gamemode = "survival"
            elif gamemode == b'\x01':
                gamemode = "creative"
            elif gamemode == b'\x02':
                gamemode = "adventure"
            elif gamemode == b'\x03':
                gamemode = "spectator"

            print(f"login (play): \n\tplayer EID: {play_user_id}\n\thardcore: {play_hardcore}\n\tgamemode: {gamemode}\n\tprevious gamemode: {prevous_gamemode}\n\tnumber of values in fallowing list: {num_in_next}")  # Login (play)  # please add to PaketDecoder.py as its massive and I want to get all small packets first
            print(f"Custom payload: \n\tserver flavor: {self.decode_packet['custom payload'](self.read_fully(connection))}")  # custom payload only works on non-pure vanilla servers
            print(f"something: {self.read_fully(connection)}")  # something
            print(f"extra: {rest_of_data}")

    def get_status(self, quiet=True):  # Gets a minecraft servers status
        if quiet != self.quiet:
            self.quiet = quiet
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection:
            connection.settimeout(self._timeout)
            connection.connect((self._host, self._port))

            # Send handshake + status request
            self.send_data(connection, b'\x00\x00', self._host, self._port, b'\x01')  # b'\x01' means get status and ignore version
            self.send_data(connection, b'\x00')  # empty packet

            # Read response, offset for string length
            data = self.read_fully(connection, extra_varint=True)
            
            # Send and read unix time in ping/pong
            self.send_data(connection, b'\x01', time.time() * 1000)  # ping
            unix = self.read_fully(connection)  # pong with server time in ms

        # Load json and return the data
        response = json.loads(data.decode('utf8'))
        response['ping'] = int(time.time() * 1000) - struct.unpack('Q', unix)[0] # adds ping response time

        return response


if '__main__' == __name__:
    stat = Server('192.168.56.1', port=55556, quiet=True, username="PythonClient")
    print(stat.get_status())
    print('\n')
    stat.offline_login()
