#!/usr/bin/python3
import socket
import struct
import json
import time
import zlib
import getpass
from PacketDecoder import packet, _Packets, _static_pack_varint, _static_unpack_varint


# will use when online mode is added (please add if you have free time [I don't have internet on my desktop, so I can't])
# import rsa

# compressed so that it is less bytes total for this file, to make
# a custom one, just replace this with json.loads(dict) where dict
# is a dictonary containing all the data (see https://wiki.vg/Server_List_Ping#Response)
pingdata = zlib.decompress(b'x\x9cMV\xc7\xae\xeb\xca\x95\xfd\x95\x8b;\xa5\x9f\xc5L\xd1\x1e\x15s\xceAT\xa3\x07\x0c\xc5L\x91b\x16\x8d\xf7\xef\xd6y\x8d\x86]\x93\x9dj\xa7\x02ja\xfd\xeb\xf7\x0e\xe7\xa5\x19_\xbf\xff\xf1\xeb_\xbf_\xe9\x00\xbf\xcao\'\x9d\xe0\xfc\x0b\xfb;\xc6\xfe\x1d\xff\xfd\xb7_\xbf\xa7y\\\xc7|\xec\x7fb\x0c\x8d\xfe\xfe\xf3\xc7\xd7\xa7\x9fo\xea_yCz~%\x85~\xdd\xe3\xabo^?EH\xf6k-\xe90\xf5?\xd6\xff\xfc\xa7\xb82\xbe\xb29\xfd)\xbbmM\xf1\xe3\xc1P&\'\xf0\x14\xfeq\xbf\x13\xf7?\xc8\x94e\xff\xc8\x88\x82\xf8\xa3\xbcg\xf4\x9d\xa0Y\x16\xcf\xd2\xdf\x7f\xfe\xefO\xd7\x02.\xf9\xdcL\xeb\xffO\xbc\xc2s\xfd)\x01~\x99\xdf\xb6\xf9\x9c\x96\xeb/\x1f\xce\xdf\xa5\xfe\x1a\xb2L\xf7&\xff\xeb\xea\xef"]\xd3\x7f4CZ\xc1\xdb\xf4\xaa\xfe\x99\xa5\x0b\xa4\xc9\xbf5\x11g{\x07\xaa\xcb\xd5\x08\xbe\xc7\xf2\xc3Z\x0c\xab\xaf&\xfe\x98\x1c\xe0\x81\xfa\xa3\xf4<\x92j_\xa9\xf0h/\xba\x91G>6\xfcI\xe0\xf70\xf2\x02\xe5b\xf0k\xd7\x04\x7f\xb2\xf6\x8d\x91\xf4\n\xd7\xee\xb1\xc4\xabIY\n%\xea\x97\x9d\x9f\xe8\xb7\xaa\x9eHS|s\xb7\x8ecE\xda\xe2\x11\xafo\x05\xde\xf0\x15\xfc\xcc\xe2qI\x1e\xc4g\x9a\xd2("\xda\xe8\xddj\xca\xb6N\x14\xd2\x12\xd6\xf5\xc4\xa1\xf2*z\xfb\x11\xf6\xf4}!,S\x17/\x8ap\x9c\rB\xb8\x85\x1b\xe5\xb1\x9f\x915\xd3\xf6Y/`\xcd\x12\xab\x92\xe6\x8c\xeb\xf8\xd5\xf0\x0cp\r\x17\xbe\xc4\x9f\xd8\xc0\xde\x17\xeeZX\x11&\xe5$\xa9Q\x91\xd7g\xab\xd1\xfb|\x15\xef\xd3u\xa8%X\xcf0\x8b$\xb0\t\x8f\x8f\xb3\xa7\xdda\x8d,\xfe\x14\xa7\xf7\xf3\xdd\x1c^\x15c*\x98rd\xc5:\x95[;m\xb9\xb2>\x7f^\x19\xb3\xd9\xfb\'\xb3\xb1\x0f\x91\xba\xa0\xd8d\xeefU\x1b\x86\x13\xf2F\xbd\xebMJ`\xc5!\xc4\xc4(\xe7\xfb\xe1\xd3\x1b\xddO\xd95\xb2n\xef\xc59\x95!Z\xff\xe6\x11[\x87Si\x89\xcai\x15*7v\xf4l\xa1\xd6\x14~\xe0\x9b\x9e>~\xb5\xb9\x9f\x16\xec\xaf\x80\xa6\x93T&\x12\xdcB\xce%\xad\xde\xa4\x02\xa2d\xc1]\xeeA:\xd3\xcb\xd3\xca\x9b\x7f\xf0\xf8\xfcN\x07f\xc9d\xac\xfb\xc8\'-\xccn\xc27\x14\x81\x9fQ\xad$\xcd0\x07\xf5l\x00\x92\xa2P8\xb3\xa2*\x8dz\xedJ\xb9\xe6\xbcC\x9aS7\xacz\x00L\xa9\xe1;\xb0D\xa9\x0c\x81Q\xa7\xd5\xd8\x84L\r\x03\xdb\x9c2\xd1\xb6D\x17\xf5=\xef\xb5U(\xea\x0fM\xf9V\xb9\xe7\xca\xd3\x17!\xca\xbd=a\x8a\xc4\xe8[<\x13\x9c\xa0b\xfb\xbab\x15B\xca\xcf`M\xc3|=\xcag0\xca\x94\x90\x00\x03K\x17dg\xfd\t\xfb\xbcD\x92D5\xc3Z{\x97Kt*\x1d\xbb\xb8z\x1aji\x8c\x8c/[\xca\xc3\xe3,u\x8b\xe8\x86D\xddW\x95K\xc8r\x1b\xc1\xc2\xdb\x08qOU\x94B\x89\x13\xe2\x14aS\x80\x13\x0f8\x1f1xx\xf7a\xa8t\xcd\x93\x01\x90n\x18\xe4wE\x9d\xf1D\xb1\'`,{/Z\xd7\x94Dx\xd1\x19\x17\x95q\xbe\'\x98V>\xfbu\x86\x1a\x96\xd8\xa0\xc1\x91x\xa3\x1czDH\xd7T\xc4F\xef\xeea\rw\x1c\xaf\xc9K\x9eDPM\x94$\x01\xe7\xde\xf2e\xaea\x13P\xac\x96I\xfd\x8f\xd9\xe0<Y\xbd\x94\x02@\xcd\xde%\xd1\x93\xa2\xf4\x93{\x99A\no\xdeT/\x8bt\x8f7\xc3\xf57N\x1c\x8bY\xf6#\xf0`\\\xa4\x87k\xc9:\xb4t\xd2Q\xdci\xb2\x13\xf2\x9a%\xc4\xa8\'d@\xad\xabN\x98\xd4\xfbJp\xa7\x9c\xedYZ\x05w \x1d&\x0c1|\x0c\x8bw\xc1\xa2x\xab\x9fq\x80\x1dx\x81\x82U\x16_\xc8\xe2\xa1\xadA[6\x86\xa0\xaa\xcf1\x8a\x8e\x9c\x1a\xc6\xe0\xa9_\xbf\xac\x83\xb9K>a\x93\xe1]\xab4cSR0\\\xaa\xf3\x0eh\xf0\x9d\xc29\x0b\xfdI\xb6&v{\xac%\xc9\x93W\xbc:\xacA\xbb4z\x0b\x93Y\xe9OB\xd1\r?\xe2\x053#\xc5\x82,\xad\xd2o\x15\xf6\xf1\x18W\x93{\xee\x80\x9e\x8a\x81\x12\x8c8pB\xa0\x08d\x96\x00\xfa2\xa6n\xd0\xcc\x8e\xffp\x0c\x1f?\xf2\x80\x98\x90\xe8=G6\x00K\xadG>\xa6\x01\xb5\x8d\x05\x0b\xe7@\xf6\x00\x8b`\xd0\xd7\xb6\xb6y\x80m\x04\xcf\x866\x06\xc54m"f\xed\x84\xb3W\x90\xa7\x0e\x9bW\x89\x16D\xa7h\xca\x94\xd1D\x05\x14(\x02\xd7\xbd\xc5:\xc8H>e\x0c\xe5\xa5\x1as\xb7~7\xc1B\xe1\xfe$\xc8J?p\x97\xd7\x0c\xf6\xf0qW\x08\x12\xa3\x11TP\x83\xef\xef\x0b|\xc0\xad\xbay\xe6\x05\xc5\x1e\x0fo\xadT8\xdc\x1f\x8c\x98\xb2n\x89H\xdc|a\x95\xf9\n\xc7[|2\xc1\x16\xc2i\xec\x85\x07H\x03\xbb\xed-\xe5\x0e\xb7\'\x0b|\xdaN\x9c\xc1vqK\x95Q\x1a\x1e\xd4\x93L\x11\xddz\x9f\xd1%W2\xd80\xd7H$\xe2\xdaG\xa0\xedc\xf6q\xc8k\x1e\xee\xcdS\x0c\x10\xc0DT_)\xcf\x1b\xc7%\x1eJ\xac*\xaa\xbb\x031\xb4O\x9c\xb9\xe4Q~\x8d\xf0\x088nh9\x89:\x93L\xe5\x98\x8fY?M\xde\x95Tq [\x87\xe2\x01\xefQO\xb0\x05_\xec(++>\xa3*\x19\xf1\xec\xea\xb6\xa7>\xd4\t\x98\xa3\xb4Q\xe5@\xf6a{\xb7\xb0\x83M\xec\xe9\xd4\xe5\xa2/sC\xe4\xbcMa\x85\xfcr\xedJ\xc95\xe3]\xa8\xa2`\x13w`\x1d\xe5\xb6\x9b"\xa2\x01\xfd"A\x98\x9dW\xc0s\xeb\xdd\x95;\xebIs\x1f\x9ad_\xb0\n^\x0f&\xc6[\xed\xea\x95p\xfbT\xc0\x0bW\x9f\xc4\xd1(\x84,\x0b\xc4\xb9\x08\xe5\xc9\x7f\xfbrOV\xcaA\xf8V\xb6\xd65\xfb.\xa3h\n\x98/\\\x7f\xa6\xfd\xc6\x0fZ^#e!\x14\xa3\x03\xf1\xfc\xa6q&.M\xf2j\x9d\xad]\xa9\xa8\xbf\x8a\x1e\x15\xd1s\xc6\xc0\x86_Y\x93@\xc8\xcd\xa6o&\xb2\xb2\'\xd7\x94\xf9q\xe7:y<Z+\x17\x9dd\x1b\xc5\x11x\xabY~bKL\xda\x19\x83\xda\xe3\xad\xd1<W"@\\\x1c\xd4\\%\x9e\xdf1\xb5!\xe0\x91\xb3\xcd\x87\xcc\\.\x1d1\xa7\xd6J\xdb)\x8f\xd2)9\xd3\xac\xf7\x1d\x08\x9e\xf0z\xf1U\x98D\xc3\x98\xa0\x97m\x8b7\xab\xa1\x0c\xef\xc9\xe7\xec.\x7f\x80\x13@\xc5\x0eS\xe3\xb1\xe5\xcb\x0b.\x8b\x13j\xea\xfa\xccq\xa2\xb1\xe3$\xf76[v!f\xd5\xf3\x15O\xee\xc83\xb9K\xcb\x85\x19\xe1\xce\xf0\xea\xb1\x9b\x80\x13,P\x02?\x0fI\xf2j\x86\x1e\xda\xde##\xf7\x0b\xc5\x1c\xca\\\xde\xe7r\xc82i\xf1X\xaa\xc7W\xa8\xd3eW\x88\xb2iB\xf3\xfd\x81\x96\xa0q:\xeb\xf7\x989\xc5z\xd7\xa68\xe2\n\xa6\xff\x88\x1f\xcea|\x98zK>v\x0cNT\xb2\xa0_\x1c\xda\xf3-f\x8d%N\x88D;\x8c\xfb\xe5\x07\x07\xbc\x9f\xf8\xfa\xc5\xf7\x109\xb8t\x17n_\x94/*\x8c_\x1e$\xddt\x1f\x8c*\x1e7\xc3\xf6\xc2\x932b\x83k\xa5\xc5\x8a\x93\xd7\x87\x98\xcb(\xdd\x9e$\xd0N\xdeq\xca\xc5\xc9\x0b.xO\x84\xd7\xd2\x931\xb1\xfc\x95\xbd\xf2\x85\x1aL4+t9\xc7[\x99\xc1\x9d\xe7F\xe7\x93\xdb\x93V\xf5\xda)\xd7\xb9W\xef\xc8\x90\xa5\xd2)\x0c\xfcN\x11\xc1\x9ed\x88\xc7\xde\x0e\xbdm\x07\x07\xb9\xec\'\xaeBf\n\xf2;\x7f\xd8\xc9\x99\x97_\x9c\x9b|\x19\x15\xfc\xd2s\x1f\xd5\xd5\xdee\xc3\xed|\xe7\x90\xa0i\x18\xf0\x96!\xb6\x9c\xb2\'\xb5c\xebRO\t\xb6R\x95N|?qy\nY\x07\x04n\xaf\xa4^\xbb\xf1u\x81s&%\xe4S\x90\xd17\x94D\xed\xddA\xf0\xfc#\xfb$\xe3\xd8\x94\xa1W\xaa\x03 \xe7T\xfd\xd0S/\xae\x06\x88\xcf\xe6S\xe7\x00\xad\xbd-\xb7\xe9\xe2FJ\x80\x93H)\xaa\x08=\x15\\5\x96\xaf\x90\xb9=\x8a\xa7\xc9}@\x84\xd06#J\x8b\xd8\x93#A\xc3\xc6\xccT\xf5\xcb\x06\xf5\xe5\xa2\x97g\xad\xd39\xe2`=\x82\x0b\xd6\xde\xcaq\rd9\x96Da\xca\xe9\r\xf3\x01?\xec\x8e\x9ek\xee\xc3\x95f+\xaf\xfb\xae\x03v\xdf\xe6D]b\xae\xb0g\xec\xd4\x81{c\xcb\xf1\x17"\xb0\xb1\xab\xbe/\x94\xb9B\x88\xb7\tH\x074\x03F\x8c{\'S)\xe4\xcd\xccn\x92t\xe7t\xeb\x87|\x01\xb1\x97\x82\xce\xdf\xdc\x81\xe7\xff\x8f\x8d\xc2\xbd\x81\xc7\xc2\xd7\xe9\x0f\xf7+\xd3~\x81_7|\x95\xe3\x9c\xc3\xc5\x87\xf96\xc3\xff\x0e\xfe\xf9o\xb4\n\x8b\xd5').decode()

if getpass.getuser() == 'runner':
    replit = True
else:
    replit = False


class Server:
    def __init__(self, host='localhost', port=25565, username='', timeout=5, quiet=True):
        # Init the hostname, port, timeout, username, etc
        self._host = host
        self._port = port
        self._username = username
        self._timeout = timeout
        self.quiet = quiet
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

    def read_fully(self, connection, extra_varint=False, return_id=False, printall=False):  # Read the connection and return the bytes
        packet_length = self._unpack_varint(connection)
        packet_id = self._unpack_varint(connection)
        if not self.quiet or printall:
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
            if printall:
                print(byte)

        if byte != b'':
            if not self.quiet:
                print(f'in\t{byte}')

        try:
            if return_id:
                return zlib.decompress(byte), packet_id
            return zlib.decompress(byte)
        except:
            if return_id:
                return byte, packet_id
                
            return byte

    def online_login(self, quiet=True):
        if quiet != self.quiet:
            self.quiet = quiet

        if self._username == '':
            raise ValueError("Username can't be blank when logging in")

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection:
            connection.settimeout(self._timeout)
            connection.connect((self._host, self._port))




    
    def offline_login(self, version="1.18.2", quiet=True):
        if quiet != self.quiet:
            self.quiet = quiet

        if self._username == '':
            raise ValueError("Username can't be blank when logging in")

        """
        0:  Handshake                            out     starts connection and gives connection data
        1:  Login start                          out     sends username
        2:  Set Compression (optinal)            in      max size before a outgoing packet must be compressed (zlib)
        3:  Login success/forge detection        in      gives data about the user after the login has succeded
        4:  Login (play)                         in      gives data about the user's entity, dimentions, gamemodes, etc
        5:  Server custom payload (Optional)     in      tells server flavor, like paper or bukkit
        6:  Change Difficulty (optinal)          in      ADD DISCRIPTON
        7:  Player Abilities (optional)          in      ADD DISCRIPTON
        8:  Client custom payload (optional)     out     ADD DISCRIPTON
        9:  Client Information (clarify)         out     ADD DISCRIPTON
        10: Set Held Item                        in      ADD DISCRIPTON
        11: Update Recipes (clarify)             in      ADD DISCRIPTON
        12: Update Tags (clearify)               in      ADD DISCRIPTON
        13: Entity Event (clearify)              in      ADD DISCRIPTON
        14: Commands                             in      ADD DISCRIPTON
        15:
        16:
        17:
        18:
        19:
        20:
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

            loginorcompression, id = self.read_fully(connection, return_id=True)

            if id == 0x03:  # setting compression # login_suc_bytes
                compression_length = self.decode_packet_login[0x03](loginorcompression)
                print(f"compression length: {compression_length}")
                login_suc_bytes = self.read_fully(connection)
                login_uuid, login_username, login_suc_bytes = self.decode_packet_login[0x02](login_suc_bytes)
                print(f"login success: \n\tuuid: {login_uuid}\n\tusername: {login_username}\n\textra:{login_suc_bytes}\n")  # Login success
                
            elif id == 0x02:  # login success, if it isn't either the server is messed up or python did some black magic again
                print("compression not set")
                login_suc_bytes = loginorcompression
            
                if b"This server has mods that require Forge to be installed on the client. Contact your server admin for more details." in login_suc_bytes:
                    print("Server has forge enabled, which I have to either find a way to spoof it and ignore the mods, or, find a way to add mods")
                    return
                
                login_uuid, login_username, login_suc_bytes = self.decode_packet_login[0x02](login_suc_bytes)
                print(f"login success: \n\tuuid: {login_uuid}\n\tusername: {login_username}\n\textra:{login_suc_bytes}\n")  # Login success

            else:
                print(f'bad packet id receved: {id}')
                return
                
            # find way to catch the error that comes from here when hitting a forge enabled srever
            play_user_id, play_hardcore, gamemode, prevous_gamemode, dimentions, rest_of_data = self.decode_packet[0x26](self.read_fully(connection))
            
            if gamemode == b'\x00':
                gamemode = "survival"
            elif gamemode == b'\x01':
                gamemode = "creative"
            elif gamemode == b'\x02':
                gamemode = "adventure"
            elif gamemode == b'\x03':
                gamemode = "spectator"
            else:
                gamemode = f"Unknown ({gamemode})"

            if prevous_gamemode == b'\x00':
                prevous_gamemode = "survival"
            elif prevous_gamemode == b'\x01':
                prevous_gamemode = "creative"
            elif prevous_gamemode == b'\x02':
                prevous_gamemode = "adventure"
            elif prevous_gamemode == b'\x03':
                prevous_gamemode = "spectator"
            else:
                prevous_gamemode = f"Unknown ({prevous_gamemode})"

            print(f"login (play): \n\tplayer EID: {play_user_id}\n\thardcore: {play_hardcore}\n\tgamemode: {gamemode}\n\tprevious gamemode: {prevous_gamemode}\n\tdimentions: {dimentions}\nnumber of bytes extra/not unpacked: {len(rest_of_data)}")  # Login (play), still wip as its massive

            print(rest_of_data)

            print(self.read_fully(connection))  # ment to be the flavor, but at this point packets are getting borked and this ends up being 1/2 of it
            packet_data = self.read_fully(connection)  # 2nd half of flavor and start of change difficutly
            # at this point im giving up
            """
            if b'\x0b' in packet_data:
                for i in range(len(packet_data)):
                    if packet_data[i] == 0x0b:
                        print(packet_data)
                        print('\n')
                        packet_data = packet_data[i:len(packet_data)]
                        id, n = _static_unpack_varint(packet_data, return_num=True)
                        packet_data = packet_data[n+1:len(packet_data)]
                        print(packet_data)
                        length, n = _static_unpack_varint(packet_data, return_num=True)
                        difficuty, locked = struct.unpack_from('c?', packet_data)
                        print(length)
                        break
            """

    def get_status(self, quiet=True, ip='', port=0):  # Gets a minecraft servers status, is fully compleated
        if quiet != self.quiet:
            self.quiet = quiet

        if ip != '':
            self._host = ip
        if port != 0:
            self._port = port
            
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection:
            connection.settimeout(self._timeout)
            connection.connect((self._host, self._port))

            # Send handshake + status request
            print("handshake")
            self.send_data(connection, b'\x00\x00', self._host, self._port, b'\x01')  # b'\x01' means get status and ignore version
            time.sleep(1)
            print("empty")
            self.send_data(connection, b'\x00', b'\x00')  # empty packet

            # Read response, offset for string length
            print("json")
            data = self.read_fully(connection, extra_varint=True)
            
            # Send and read unix time in ping/pong
            print("ping")
            self.send_data(connection, b'\x01', time.time() * 1000)  # ping
            print("pong")
            unix = self.read_fully(connection)  # pong with server time in ms

        # Load json and return the data
        print(unix)
        print(data.decode())
        response = json.loads(data.decode())
        if type(response) is not dict:
            response = json.loads(response)
        print(response)
        print('\n', type(response))
        response['ping'] = int(time.time() * 1000) - struct.unpack('Q', unix)[0] # adds ping response time

        return response

    def honey(self, serveraddr=socket.gethostbyname(socket.gethostname()), serverport=25565):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.bind((serveraddr, serverport))
            server.listen(10)
            working = True
            print(f"started honeypot on {serveraddr}:{serverport}\n")
            while working:
                try:
                    client, addr = server.accept()

                    print(f"{addr[0]}:{addr[1]} connected")
            
                    version, is_ping = _Packets.client.handshake(self.read_fully(client))
            
                    if is_ping:
                        print(f"{addr[0]}: request, ping")

                        print("reading nothing")
                        self.read_fully(client)  # empty packet
                        data = json.dumps(pingdata).encode()
                        length = _static_pack_varint(len(data))

                        print("send json")
                        client.send(length + b"\x00" + length + data)

                        print("ping")
                        data = self.read_fully(client, printall=True)
                        print(f"ping: {data}")
                        print("pong")
                        length = _static_pack_varint(len(data))
                        client.send(length + b"\x01" + data)  # pong
                        print(f"{addr}: disconnected\n")
                        client.close()
                    else:
                        print(f"{addr[0]}:{addr[1]}: request, login")
                        
                        if version > 1528:  # they are a higher version
                            client.send(_Packets.client.disconnect("outdated server! I'm still on 1.19.2."))
                            print(f"{addr}: responce, outdated server, version: {version}")
                            print(f"{addr}: disconnected\n")
                            client.close()
                            
                        elif version < 1528:  # they are outdated
                            client.send(_Packets.client.disconnect("outdated client! I'm on version 1.19.2"))
                            print(f"{addr}: responce, outdated client, version: {version}")
                            print(f"{addr}: disconnected\n")
                            client.close()
                            
                        else: # they are the same version and attempting to connect
                            print(f"\n{addr}: data, ", _Packets.Client.loginstart(self.read_fully(client)), "\n")  # just id data (like username, uuid, etc)
                            
                            # skipping encryption request, idk how to work mc's auth servers, but maby you can add this
                            
                            # skipping compression, because we only need to send one more packet and don't start Play mode
                            client.send(_Packets.client.disconnect("Invalid encryption response!"))
                            print(f"{addr}: disconnected\n")
                            client.close()
                except KeyboardInterrupt: 
                    working = False
                    print("finishing last client before exiting")
                    
                #except Exception as err:
                    #print(f"\nError encountered, continuing\nError: {err}\n")

if '__main__' == __name__:
    stat = Server()
    print(socket.gethostbyname(socket.gethostname()))
    stat.honey("0.0.0.0", 8080)
