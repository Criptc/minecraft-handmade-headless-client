#!/usr/bin/python3
import socket
import struct
import json
import time


class Server: # took this from a minecraft server status finder 

    def __init__(self, host='localhost', port=25565, username='', timeout=5):
        # Init the hostname, port, timeout and username (username not needed yet)
        self._host = host
        self._port = port
        self._username = username
        self._timeout = timeout

    @staticmethod
    def _unpack_varint(sock): # Unpacks a varint
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
    def _pack_varint(data): # Packs the var int
        ordinal = b''

        while True:
            byte = data & 0x7F
            data >>= 7
            ordinal += struct.pack('B', byte | (0x80 if data > 0 else 0))

            if data == 0:
                break

        return ordinal

    def _pack_data(self, data): # packs data into a packet
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

    def _send_data(self, connection, *args): # Sends the packet to the server
        data = b''

        for arg in args:
            data += self._pack_data(arg)

        print(self._pack_varint(len(data)) + data)

        connection.send(self._pack_varint(len(data)) + data)

    def _read_fully(self, connection, extra_varint=False):
        """ Read the connection and return the bytes """
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

        return byte

    def login(self): # logs into the minecraft server (WIP and currently not working)
        # start socket, set the timeout and connect to the minecraft server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection:
            connection.settimeout(self._timeout)
            connection.connect((self._host, self._port))

            # handshake and setup login
            self._send_data(connection, 0x00, 758, self._host, self._port, 2) # handshake packet:  connection, packet id (must be 0), protocol version (must be servers version otherwise you get an error), server ip, server port, login (2, if its 1, you get the server status {use get_status})
            print(self._read_fully(connection))  # currently need to fix version error, says: b'C{"extra":[{"text":"Outdated client! Please use 1.18.2"}],"text":""}'
            # will add more after handshake is fixed

    def get_status(self): # Gets a minecraft servers status
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection:
            connection.settimeout(self._timeout)
            connection.connect((self._host, self._port))

            # Send handshake + status request
            self._send_data(connection, b'\x00\x00', self._host, self._port, b'\x01') # b'\x01' means get status and ignore version
            self._send_data(connection, b'\x00') # empty packet

            # Read response, offset for string length
            data = self._read_fully(connection, extra_varint=True)
            
            # Send and read unix time in ping/pong
            self._send_data(connection, b'\x01', time.time() * 1000) # ping
            unix = self._read_fully(connection) # pong

        # Load json and return the data
        response = json.loads(data.decode('utf8'))
        response['ping'] = int(time.time() * 1000) - struct.unpack('Q', unix)[0] # adds ping response time

        return response


if '__main__' == __name__:
    stat = Server(input('server address: ')) # ask user for the server address, but not for port as most servers use defult port
    stat.login() # logs into the server
    
