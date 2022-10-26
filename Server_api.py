#!/usr/bin/python3
import socket
import struct
import json
import time

# will use when packet sending added
# import zlib

# will use when online mode is added (please add if you have free time [i dont have internet on my desktop])
# import rsa


class Server:
    def __init__(self, host='localhost', port=25565, username='', timeout=5, quiet=True):
        # Init the hostname, port, timeout and username (username not needed yet)
        self._host = host
        self._port = port
        self._username = username
        self._timeout = timeout
        self.quiet = quiet

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
        print(packet_length)
        packet_id = self._unpack_varint(connection)
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
        if return_id:
            print(hex(packet_id))
            return byte
        else:
            return byte

    def login(self, quiet=True):
        if quiet != self.quiet:
            self.quiet = quiet

        # start socket, set the timeout and connect to the minecraft server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection:
            connection.settimeout(self._timeout)
            connection.connect((self._host, self._port))

            # handshake and setup login
            self.send_data(connection, b'\x00', 1526, socket.gethostname(), self._port, b'\x02')  # handshake
            self.send_data(connection, b'\x00', self._username)  # login
            self.read_fully(connection)  # max packet length until compression
            print('\n')
            # unknown
            self.read_fully(connection)
            print('\n')
            self.read_fully(connection, extra_varint=True)
            print('\n')

    def get_status(self, quiet=True):  # Gets a minecraft servers status
        if quiet != self.quiet:
            self.quiet = quiet
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection:
            connection.settimeout(self._timeout)
            connection.connect((self._host, self._port))

            # Send handshake + status request
            self.send_data(connection, b'\x00\x00', self._host, self._port, b'\x01')  # b'\x01' means get status and ignore version
            self.send_data(connection, b'\x00') # empty packet

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
    stat = Server('192.168.56.1', quiet=True)
    print(stat.get_status())
    print('\n')
    stat.login(quiet=False)
