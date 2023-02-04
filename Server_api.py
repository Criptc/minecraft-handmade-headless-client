#!/usr/bin/python3
from PacketDecoder import packets, _static_pack_varint
from Crypto.Cipher import AES
from getpass import getpass
from hashlib import sha1
import requests
import base64
import socket
import struct
import json
import time
import zlib
# import rsa
import os

# compressed so that it is fewer bytes total for this file, to make
# a custom one, just replace this with json.loads(dict) where dict
# is a dictionary containing all the data (see https://wiki.vg/Server_List_Ping#Response)
pingdata = {
    "version": {
        "name": "Paper 1.18.2",
        "protocol": "758"
    },
    "players": {
        "max": 50,
        "online": 49,
        "sample": [{
            "name": "HACKER",
            "uuid": "107c32ae-8838-4a99-b3d3-f8b6836992ba"
        }]
    },
    "description": {
        "text": "A fake Minecraft Server"
    },
    "favicon": "data:image/png;base64," + base64.b64encode(zlib.decompress(b'x\xda\x01D\x07\xbb\xf8\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00@\x00\x00\x00@\x08\x02\x00\x00\x00%\x0b\xe6\x89\x00\x00\x07\x0bIDATx^\xed\x99\xdfo\x14U\x14\xc7\xcf\xbd\xb3\xbc\x90\xd2\xa4\xdb\xee\xecR\xa0\xd8\x9f\x16\x14"\x18}\xf0\xdf\xd1\'\xe4I\x82\xbf\x82\x1ax0J\x81\xfe@}\x13\xa3B\xf9\x19c\x0c"\xd2\x1fl[Z\x8b\x18_|\xa9\xa5\xa5U\xde5j\x8c\x91\xee\xb6\x9e~\x8fssgg\x87\x9d\xd9N]Iz\xf2\xcd\xcd0\xa13\xe7s\xcf\xb9\xe7\x9e\xb9K\xb9G\xdc\xa8\xf4\xc6\xa3f\x1b\x00\xb5\xb6\r\x80Z\xdb\x06@\xad-\x12\xc0\xcel\xf6\xb1l\x96/Z\xb3\xd9\x03uuF\x1f\xa4R\x15u\xc8q\x8c\x9e\xaf\xaf7j\xc5\x03\xf9\xb1;qQ\xb5E\x02\xe0\xd7\xc8\xfb\xda\x93\x03h\xf7fD\xa6\xa6j\x8b\x04`[R\x00\xa5\xcf\xad\xd6B\x01\xb6Bl\xcd\xb9\\g6\xfb\xb8\xeb\xf2l\xedr\xdd\xa4\x00v\xe1\x81\xfc\xd8.\xd7m\xc6\xbb\x9a\xa1\xb8V\x1e\x80\x1f\xb7\xa7\xb1\xf1\xa9t\xba\xbb\xa9io:=BTVs\x96\xfe&Z\x82\xf8\xe2\x9e\xa5\xf3D\x1f\x13] \x1a$\xea\xb3t6\x952z\xae\xa9\xc9(.C(\xc0\xbet\xfa\xe9\x86\x86\xdd\x8d\x8d\xfb\x1b\x1a\x82\xae\x07\x01V,\xd9\x00W\xe0\xfagD\x97\xffK\x00\xb6\xae\xa6\xa6\xee\xc6\xc6\xd6L\x86\xc7\xa0\xebA\x80\xa2\xe7}\xb1V\x11\xd8\x8aj\xd3\x86\xb2\xc0\xe3\x9etz\xbfD Z\n\x85\x01\\$\xfa\x94\xe8\x12.\xd6\x05\xc0\xd4x^\xa93D\x15\xf5\x00.\x16\xa0\xa2%;\x85\xe4\xce2\x96\xc48\xd1\x10\xd1$Q\x9e\xe84\xd1)\xa2~\xa2\x01f\xd0\xba\xcfq\x06\x94\xeau\x1c^\xca\xb9j\xf7\x0425\xbe\xdbu\x83\xee\x06e;ZQ\xcbp}\x94\xe8\x1b\x90\xd8\x00\xbdZ\xb3\xeb\xfdJ\x9dr\x9cN8\xd0\x92\xcd\xb6T\x01`\xaeZ\xa2E\xa0d\xb2\x1f.\x8e\xd2\x18\xd1\xd7D\x13H\xb9^\xa2\xe3D\'\x81\xc1~\xb3\xfa\x00\xb0#\xbe\xdf\xc6\x88\xd3\x9d7\xc5\xed\xb9\xdc\xee@\x04L\x1e\xaf\x05\x80]\x1f&\x9a\x02\x89D`\x00\x17\xfd^\n\xf1\xc8\xaff\x07:\x90\x0b\xb2\xf9D7:XWgd/>[\x05$C0\xd7+J\x16\xf4,\xd1"\xd1<\x18F\x81\x94Gu:\x87\x95}V\xa9\x176o6\xda\x1e3\x1a\x91\x00\x82\x9eE\x14\x03\xfc\x8c\'\xdc\'Z@\x1c\xd8\xfbi,\x8c\x8b`\xb8\x82q\xdd\x01\xe2N\xbcQ\x11\x15V\xb2q\x16\xcb\xe0:\x820\x8c\xcd\xe1\x0c*\xec\x19\x7f\x04J\x1d\xacd\x95\x01~\xd0\xfaW\xad\x7f\xd3\xfa\x17\x1e\x95ZBF=@\x8945\xb4D6\xc0"\x18$\x0e\x92<\xb7pq\x19\xbb\xdbj\x04\xfc\x00\\\x0cyMv\xa1Gjw\xdd6\x8c\xacVO\\6w@-\x18I\xfe\xb1\x1d#/\xa3N\xd7\xed\x08H\x1e\xc7+\xecI\xd7\xbd\x9aJ\x19\xcd\xc3\xbf\x05Ks\xb8S\xc2`$\xbb\x87h\t\xb3 \xfa\x93\xe8\x0f\xa5x\xfc])\x9e#3_\xd7\xb5\xfe\x02\xe35\xad?\xd2\xfaC\xad?Q\x8a\xc7\x97\x1d\xc7(\xb4\x95\x083\x1b\xe0Gx|\xd7\xd2\x8c\x7fW^\x8bL\x05\x9b\xc0\xea\x97f\xe42\xd6L\xf5\x00\x1c>\x1b`\x0e\xb3.\x99&$\xc9\x02\xc8\x1e\xc2Yw\x13\xde\x9f\x95\xaa\xb5N\x00\x0b!)T\xb5$\x02#X3v\x04\x06\xd7\x02\xc0\xcb\xeb;\xad\x8d\xc4\xf5\xbbp\xbdP\xed^\x11\xa6\xa2W\xbbd\x0f\x19G\xf9\x92\x9e\x8aw\xf4wy\x07$z[\xebx\x00\x1d\xe1\x00A\x0f\xd6(\x06\xf8\t\xae\xcb\x1er\x0b\xaeKO\xc5\xddT\x0f\xc6w\xe2\x02\xb0\xd9\x00\x89/\xdc\x12\xd9\x00\xd3`\xb8\x83 \x08@\x1f\x1a\x93H\x00m(\xcc\\w\x9fp]\x1b`!\xe9\xbc_\xb1\x1a\xf5\x07\xfe\x14\x1a\xf3\xd6\x03\'R\x8f\xd6\xc7\xb4\xeeQ\xeah\x945\xc0i3\xa3\x94\xd1\xfcz\xe6}\x01.\x8e`\xf9\x8eCcH\x1bN\x9e\xc3\x96xk\xe2\x8d\xab\x15s\x1a\x01\x80\xbbT\x0b`]\xf3\xbe\x80\t\xbe\x86\xf2?\x8c\xeb\x9b\xc8\x99\x11?\x80\xed^e\x80v\x7f\x04\x16\x11\xd3{H\xd0\xa4&\xdeh\xd9\xdb\xbc\xc6\xa0i\xe8{\x04\xc1\x06h\xc1\x17\x9cXl\x80{\xc8\xc8Y0$\x05 I\xb8\x8c\xfeB\x00$yd\x0b\x93o:\x1f\x80\xd5\xb1V\x06(\xd9\xbc\xe4\xb9\x92\xa6\x85\x80+U\xa8\x88\x191\x92z?\r\xd7\x0fX:\x9cJ\x19\xd9_p\xb1\x01F\xe1\xfd\r\xcc\xd0:\x01\xdc$\xba\x9d @\xce\xdf\xc0\r\xc1\xfb\xaf0O\x89\x00\xac\xf8\x01F\xf1\xcd0\x81\xb7\xc4\x06\x90\xd6z\x07.\xb8\xf6w\xa0Nu\xfb[h\xc9\xceQ\xd4\xbb(\x00EKR\xe3m\x15Q\xef}\x00J\xddPjR\xa9!\xa5\xe2\x01\xf0\xdd#[\xb6\x18}\xa9\xf5U\xa5>\xe7v\\\xa9\xbf\xf0\xa6%\xc8~}\xd0\xdd\xa0\xf7\xb6s\xf2A3ai\x1a\xd3q\x8c\xe8\x08\xd1+DG\x95z\xad\xbe\xde\x88+}3\x7f\xb8\xb8\xee\xbf3\xeb}\xc4\x18\x9fs\x0f\x01\x90j0\x8c\xd7\x04=\x8b\xa8\x12\x80\x11\xb4\xc7\xf2X\xd1\x18\x8e\xbd^%z\x89\xe8 _\xf8\x01,?C-\x14 \xaf\xd4\x88\xb7{\x07=\x8b.\x1b@\x16\xa8\xd4\xf8I|\xe3\xdf\xc1\xf3\xdf\x04\xc3!\xbe\xf0\x03D9\xe7\n\x05\x18Vj\x18\xd33\x8e\x13\xf3b\xe4\xb4Y\t\xcfo\x1b \x0fM\xe1\xceQ\xa2\xd7\xb9\xcb\'z\xcb\x0fP\x92-e\xcd\xb7\x88\xe5\x98q\x1b\x8e\x19\x07\xb56\x1a\xf3Z\x94(\x0b\xb7\x10\xe8gLWc\xe6\x9e]\x7f\x0fm\xfd\x00t\xd2qN8\xce)\xa5x\xe4Wo\x8b\xf3\xd3S\xf92\xca\xb1\xb3\x01\x86\xe0\xd0\xb5h\xa5\xb3P\xae\x9f\x91\xd1\x060\xc7\x8c\xab\'\x8d\x0c\x90J\xf5)u2\x95\x8a\x926\xb6\xf9\x00\xccIu\x97?\x02\xf2\xee\x1b\x98\xc8\xe5\x80\xc7AMy\'p%\x9a\x84n#D\xa7\xe1z?\xb4:\xf7\xdc\x1e\xf3\x1d\xad\xe3\x9eT\xfb\x00Z\xbc?\xeb\xf4G`\xd4+\x17\xe3\xa8\xa4\xcb^]_\xf2\xceELy-b\xc1\x8c[\rY\x89\xf2\xde\xb7\xd5j\xe6x\x00\x9cB<\xf7\xec=\xc7AN\xaawF>\xa9.\x9fB\xcd\xb9\xdc\xb3\x99\x8c\xd1\xb7J\x19\xcd\xa3\x1b\xbd\x8ff\xee\x9c\xa5\tx6\t\xef\xe5\x03\xfc\x82\xa5K\x18W\xcft\xbd\xbc\xe7t\xefa\xbf\x91\xf7\xfc\n\x8e9\x8f\xfb3\x99\xd8\x87\xbb\xa57<\x0b\x03\x98\xc5\xc7\xc0"\x1aR\x1b@\xd2}\x14\x17\x838\xfc\x18\xb4$H\xfc\x05x\xc2\xcb{\xf6\xfe8f\xbd\xc7\x9b\xf5\xb6\xc8ic[y\x80\xad\xe1\x00w\xf1\r\xb9\x00\x0c\x1b\xe0\x16R\x7f\n\x17v\x04\xceCr\x94\xdb\xeb\xfd8\xd0\xeb\xcf\xfbg2\x19.;<\xeeK*\x02\x0f\x01\xe0O\x82Y\xa5\xe6pa\x03\xe4\xbdr\x99\x0f\x00\x98\xff\xb3\xfas\x06\x8eCz\x919\x1c\x81\x1eD\x803\x87W-{\xbf\xd7u\x93\x01\xc8\x05~\xe8\xee\xc4\x16\xc1%\xe2\x8d\xfaz#\x1b \x8a^\xac\xab3\xea\xc6a+\xa7>?Y~\xd83o\x8ce\xa1\x00a\x96\x14@\xe9s\xab\xb5H\x00\xa6\xbc\xf2\x9c%\x05\xd0\x16\xb3\\\x86Y$\x00\xe9csx_\xd5\x00\xefo\xdad\x03\xc8\x8e\x19l\x8f\xe3Z$\x80\xff\xb3m\x00\xd4\xda6\x00jm\x1b\x00\xb5\xb6G\x1e\xe0\x1f\x8f\xcco\xf1E\xf0\x12\x8d\x00\x00\x00\x00IEND\xaeB`\x82\xd9*k\xa2')).decode(),
    "previewsChat": False,
    "enforcesSecureChat": False
}


class Server:
    def __init__(self, host='localhost', port=25565, username='', timeout=5, quiet=True):  # ik that taking password as a var isnt secure, i will fix it later
        self._host = host
        self._port = port
        self._client_token = os.urandom(4)
        self._username = username
        self._timeout = timeout
        self.quiet = quiet
        self.compression_length = 0
        self.encrypt = False

    @staticmethod
    def _unpack_varint(sock, ret_i=False):  # Unpacks a varint
        data = 0
        for i in range(5):
            ordinal = sock.recv(1)

            if len(ordinal) == 0:
                break

            byte = ord(ordinal)
            data |= (byte & 0x7F) << 7 * i

            if not byte & 0x80:
                break

        if ret_i:
            return data, i
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

        if self.compression_length != 0 and len(data) > self.compression_length:
            data = zlib.compress(data)

        if self.encrypt:
            data = self.aes.encrypt(data)

        if not self.quiet:
            print(f'out\t{data}')

        connection.send(data)

    def read_fully(self, connection, extra_varint=False, return_id=False, printall=False):  # Read the connection and return the bytes
        packet_length, n = self._unpack_varint(connection, ret_i=True)
        packet_length += n - 1
        packet_id = self._unpack_varint(connection)
        if not self.quiet or printall:
            print(f"\n{packet_length}")
            print(packet_id, hex(packet_id))
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

    def packcheck(self, connection, return_id=False):
        data, id = self.read_fully(connection, return_id=True)

        if id == 23:
            raise Exception(f"Client was disconnected (0x17 packet in login phase): {data}")
        elif return_id:
            return data, id
        else:
            return data

    def online_login(self, quiet=True):
        if quiet != self.quiet:
            self.quiet = quiet

        if self._username == '':
            raise ValueError("Username can't be blank when logging in")

        if os.getenv("PSWRD") != '':
            print("PSWRD environment variable not found")
            paswrd = getpass("Minecraft account password: ")

        req = requests.get(f"https://authserver.mojang.com/authenticate", headers={"Content-Type": "application/json"}, data=json.dumps({"agent": {"name": "Minecraft", "version": 1}, "username": self._username, "password": paswrd, "clientToken": self._client_token, "requestUser": False}))
        code = req.status_code
        userdata = req.json()
        req.close()

        del paswrd  # don't want to keep the users password in memory just incase

        print(code)
        print(userdata)
        exit(0)

        if code != 200: # doesn't account for a 400 for invalid time stamp, but we aren't using timestamps
            raise LookupError(f"Error with authenticating: {userdata}")

        self.access_token = userdata["accessToken"]
        username = userdata["selectedProfile"]["name"]
        useruuid = userdata["selectedProfile"]["id"]
        print(f"User authed:\n\tusername: {username}\n\tuuid: {useruuid}\n\ttoken: {self.access_token}")

        exit(0)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection:
            connection.settimeout(self._timeout)
            connection.connect((self._host, self._port))

            self.send_data(connection, b'\x00', 1526, socket.gethostname(), self._port, b'\x02')  # 1.18.2
            self.send_data(connection, b'\x00', username, True, useruuid)

            packet_data = self.read_fully(connection)
            serverid, pubkey, token = packets.Decode.login_0x01(packet_data)

            self.key = os.urandom(16)
            self.aes = AES.new(self.key, AES.MODE_EAX)

            epubkey = self.aes.encrypt(pubkey)
            everify = self.aes.encrypt(token)

            while len(epubkey) < 128:
                epubkey += b'\x00'

            while len(everify) < 128:
                everify += b'\x00'

            self.send_data(connection, b'\x01', len(epubkey), epubkey, len(token), token)

            hash = sha1()
            hash.update(serverid)
            hash.update(self.key)
            hash.update(epubkey)
            hash = hash.hexdigest()

            req = requests.post("https://sessionserver.mojang.com/session/minecraft/join", headers={"Content-Type": "application/json"}, data=json.dumps({"accessToken": "<accessToken>", "selectedProfile": "<player's uuid without dashes>", "serverId": "<serverHash>"}))

            packet_data = self.read_fully(connection)  # currently hoping the server has compression lol
            self.compression_length = packets.Decode.login_0x03(packet_data)
            print(f"compression length: {self.compression_length}")

            packet_data = self.read_fully(connection)
            login_uuid, login_username, login_suc_bytes = packets.Decode.login_0x02(packet_data)
            print(f"login success: \n\tuuid: {login_uuid}\n\tusername: {login_username}\n")

            play_user_id, play_hardcore, gamemode, previous_gamemode, dimensions, rest_of_data = packets.Decode.play_0x26(self.read_fully(connection))

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

            if previous_gamemode == b'\x00':
                previous_gamemode = "survival"
            elif previous_gamemode == b'\x01':
                previous_gamemode = "creative"
            elif previous_gamemode == b'\x02':
                previous_gamemode = "adventure"
            elif previous_gamemode == b'\x03':
                previous_gamemode = "spectator"
            else:
                previous_gamemode = f"Unknown ({previous_gamemode})"

            print(f"login (play): \n\tplayer EID: {play_user_id}\n\thardcore: {play_hardcore}\n\tgamemode: {gamemode}\n\tprevious gamemode: {previous_gamemode}\n\tdimentions: {dimensions}\nnumber of bytes extra/not unpacked: {len(rest_of_data)}")

    def offline_login(self, version="1.18.2", quiet=True):
        if quiet != self.quiet:
            self.quiet = quiet

        if self._username == '':
            raise ValueError("Username can't be blank when logging in")

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

            loginorcompression, id = self.packcheck(connection, return_id=True)

            if id == 0x03:  # setting compression # login_suc_bytes
                self.compression_length = packets.Decode.login_0x03(loginorcompression)
                print(f"compression length: {self.compression_length}")
                login_suc_bytes = self.packcheck(connection)
                login_uuid, login_username = packets.Decode.login_0x02(login_suc_bytes)
                print(f"login success: \n\tuuid: {login_uuid}\n\tusername: {login_username}\n")  # Login success

            elif id == 0x02:  # login success, if it isn't either the server is messed up or python did some black magic again
                print("compression not set")
                login_suc_bytes = loginorcompression

                login_uuid, login_username = packets.Decode.login_0x02(login_suc_bytes)
                print(f"login success: \n\tuuid: {login_uuid}\n\tusername: {login_username}\n")  # Login success
            else:
                print(f'bad packet id receved: {id}')
                return

            # find way to catch the error that comes from here when hitting a forge enabled srever
            data, n = self.packcheck(connection, return_id=True)
            print(n)
            play_user_id, play_hardcore, gamemode, prevous_gamemode, dimentions, _ = packets.Decode.play_0x26(data)

            rest_of_data = ''

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
        response['ping'] = int(time.time() * 1000) - struct.unpack('Q', unix)[0]  # adds ping response time

        return response

    def server(self, serveraddr=socket.gethostbyname(socket.gethostname()), serverport=25565, version="1.18.2"):
        if version == "1.18.2":
            version = 758
        elif version == "1.19.2":
            version = 760

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.bind((serveraddr, serverport))
            server.listen(10)
            working = True
            print(f"started on {serveraddr}:{serverport}\n")
            while working:
                try:
                    client, addr = server.accept()
                    self.compression_length = 0

                    print(f"{addr[0]}:{addr[1]} connected")

                    vers, is_ping = packets.Client.handshake(self.read_fully(client))

                    if is_ping:
                        print(f"{addr[0]}: request, ping")

                        self.read_fully(client)  # empty packet (b'\x02\x00\x00', size + \x00\x00)
                        data = json.dumps(pingdata).encode()
                        length = _static_pack_varint(len(data))

                        client.send(length + b"\x00" + length + data)

                        data = self.read_fully(client)
                        print(f"ping: {data}")
                        length = _static_pack_varint(len(data))
                        client.send(length + b"\x01" + data)  # pong
                        print(f"{addr}: disconnected\n")
                        client.close()
                    else:
                        print(f"{addr[0]}:{addr[1]}: request, login, version: {vers}")

                        if vers > 1526:  # they are overdated
                            self.send_data(client, packets.Client.disconnect("outdated server! I'm still on 1.19.2."))
                            print(f"{addr}: responce, outdated server, version: {version}")
                            print(f"{addr}: disconnected\n")
                            client.close()
                            continue

                        elif vers < 1526:  # they are outdated
                            self.send_data(client, packets.Client.disconnect("outdated client! I'm on version 1.19.2"))
                            print(f"{addr}: responce, outdated client, version: {version}")
                            print(f"{addr}: disconnected\n")
                            client.close()
                            continue

                        else:  # they are the same version and attempting to connect
                            data = self.read_fully(client)
                            print(data)
                            print(f"\n{addr}: data, ", packets.Client.loginstart(data), "\n")  # id data

                            # skipping encryption request, idk how to work mc's auth servers

                            self.send_data(client, packets.Client.setcompression(256))

                            self.send_data(client, packets.Client.disconnect("Invalid encryption response!"))
                            print(f"{addr}: disconnected\n")
                            client.close()
                except KeyboardInterrupt:
                    working = False
                    print("finishing last client before exiting")


if '__main__' == __name__:
    stat = Server("10.0.0.27", 55556, "CripticCode")
    stat.offline_login(quiet=False)
