#!/usr/bin/python3
import socket
import struct
import json
import time
import rsa
import os


class Server:  # took this from a minecraft server status finder

    def __init__(self, host='localhost', port=25565, username='', timeout=5):
        # Init the hostname, port, timeout and username (username not needed yet)
        self._host = host
        self._port = port
        self._username = username
        self._timeout = timeout

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
    def _pack_varint(data):  # Packs the var int
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

    def _send_data(self, connection, *args):  # Sends the packet to the server
        data = b''

        for arg in args:
            data += self._pack_data(arg)

        data = self._pack_varint(len(data)) + data

        print(data)

        connection.send(data)

    def _read_fully(self, connection, extra_varint=False):  # Read the connection and return the bytes
        packet_length = self._unpack_varint(connection)
        packet_id = self._unpack_varint(connection)
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
            print(byte)
        return byte

    def login(self):  # logs into the minecraft server (WIP and currently not working)
        # start socket, set the timeout and connect to the minecraft server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection:
            connection.settimeout(self._timeout)
            connection.connect((self._host, self._port))

            # handshake and setup login
            self._send_data(connection, b'\x00', 1526, socket.gethostname(), self._port, b'\x02') # 1.18.2 real version number is 1526 for some reason
            self._send_data(connection, b'\x00', self._username)
            data = self._read_fully(connection, extra_varint=True)
            # data = b'\x1e\x00\x02B\xed\xdaUi\xbf;f\xb8h\xee[,.I\x13\x0bCripticCode\xc2\x12\xb8\xbb\x01x\x9c\xed\x9c_\x8c\xdcF\x1d\xc7g\xb3\xb7\x97\xbd\xbd^\x92&\x97\xbb^\xd2rI\xd3$\xb4\x94+p\xfci\xda^/\x08\x15^\n\xe2\x8d\'d\xcd\xda\xe3\xdd\xc9\xd9\x1ek\xc6\xbb{\xdbRq-*\xcf<!\x82D\t\x7f\x0b\x0f<\xf0\\\xa9\xcd[U)\x15O \x84\x10B\x887\x04\xa2<\xf0z\x8c\xd7\xeb\xf5\x8cw|\xb6oo\xc3:\xe7<\\\xb4\xde\x9f\xe7\xcf\xe7\xf7\xf5of~3\xebk\x00\xcc\xbd\x03\xc0~\xf5\x9c\x8d\x1d\xa4Shz\xcf\x91.\xa2=B-c9\xba\xe6\xb5\x91\xe6 \xfe\x97>,_D\x8e\xd1\x00\xa0\x01\x1e\x89.\x1b\xd8F\x0e\xc3\xc4\xd1\xbc\xbe\x8b\xea`\xce\xff/\xd9`\x01\xd4\xba\xd0\xea ^\x0c\x98\xe3\xd6\x0e\xb4\x11P5\xa7\nN`\x83\x1b\xf1\xdaN"\x0b\xf12\xbc:h`\xc7\xc4\x0env\xa8\x03\xd6\xafDwE\x97\xb5Q\x01u~\x9fi"\xddc\xca\xf2+`\xa1cy\x14\xf6 \xb5A\x15\x9c\xb2H'

    def get_status(self):  # Gets a minecraft servers status
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection:
            connection.settimeout(self._timeout)
            connection.connect((self._host, self._port))

            # Send handshake + status request
            self._send_data(connection, b'\x00\x00', self._host, self._port,
                            b'\x01')  # b'\x01' means get status and ignore version
            self._send_data(connection, b'\x00')  # empty packet

            # Read response, offset for string length
            data = self._read_fully(connection, extra_varint=True)

            # Send and read unix time in ping/pong
            self._send_data(connection, b'\x01', time.time() * 1000)  # ping
            unix = self._read_fully(connection)  # pong with server time in ms

        # Load json and return the data
        response = json.loads(data.decode('utf8'))
        response['ping'] = int(time.time() * 1000) - struct.unpack('Q', unix)[0]  # adds ping response time

        return response


if '__main__' == __name__:
    stat = Server(input('Minecraft server address: '), username=input('Minecraft username: '))
    stat.login()
