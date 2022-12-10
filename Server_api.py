#!/usr/bin/python3
import socket
import struct
import json
import time
import zlib
from PacketDecoder import packet, _Packets, _static_pack_varint


# will use when online mode is added (please add if you have free time [I don't have internet on my desktop, so I can't])
# import rsa

# compressed so that it is less bytes total for this file, to make
# a custom one, just replace this with json.loads(dict) where dict
# is a dictonary containing all the data (see https://wiki.vg/Server_List_Ping#Response)
pingdata = zlib.decompress(b'x\x9cMV\xc7\xae\xeb\xca\x95\xfd\x95\x8b;\xa5\x9f\xc5L\xd1\x1e\x15s\xceAT\xa3\x07\x0c\xc5L\x91b\x16\x8d\xf7\xef\xd6y\x8d\x86]\x93\x9dj\xa7\x02ja\xfd\xeb\xf7\x0e\xe7\xa5\x19_\xbf\xff\xf1\xeb_\xbf_\xe9\x00\xbf\xcao\'\x9d\xe0\xfc\x0b\xfb;\xc6\xfe\x1d\xff\xfd\xb7_\xbf\xa7y\\\xc7|\xec\x7fb\x0c\x8d\xfe\xfe\xf3\xc7\xd7\xa7\x9fo\xea_yCz~%\x85~\xdd\xe3\xabo^?EH\xf6k-\xe90\xf5?\xd6\xff\xfc\xa7\xb82\xbe\xb29\xfd)\xbbmM\xf1\xe3I\xb1\x0c\xcbh\x96\xfd\x03\xe6y\xf1\x07\x01i\xf6\x0f\x96\xc4\xe9?\xb22\xc7\n2\xcf\xa8\x9c"~\xff\xf9\xbf?]\x0b\xb8\xe4s3\xad\xff?\xf1\n\xcf\xf5\xa7\x04\xf8e~\xdb\xe6sZ\xae\xbf|8\x7f\x97\xfak\xc82\xdd\x9b\xfc\xaf\xab\xbf\x8btM\xff\xd1\x0ci\x05o\xd3\xab\xfag\x96.\x90&\xff\xd6D\x9c\xed\x1d\xa8.W#\xf8\x1e\xcb\x0fk1\xac\xbe\x9a\xf8cr\x80\x07\xea\x8f\xd2\xf3H\xaa}\xa5\xc2\xa3\xbd\xe8F\x1e\xf9\xd8\xf0\'\x81\xdf\xc3\xc8\x0b\x94\x8b\xc1\xaf]\x13\xfc\xc9\xda7F\xd2+\\\xbb\xc7\x12\xaf&e)\x94\xa8_v~\xa2\xdf\xaaz"M\xf1\xcd\xdd:\x8e\x15i\x8bG\xbc\xbe\x15x\xc3W\xf03\x8b\xc7%y\x10\x9fiJ\xa3\x88h\xa3w\xab)\xdb:QHKX\xd7\x13\x87\xca\xab\xe8\xedG\xd8\xd3\xf7\x85\xb0L]\xbc(\xc2q6\x08\xe1\x16n\x94\xc7~F\xd6L\xdbg\xbd\x805K\xacJ\x9a3\xae\xe3W\xc33\xc05\\\xf8\x12\x7fb\x03{_\xb8kaE\x98\x94\x93\xa4FE^\x9f\xadF\xef\xf3U\xbcO\xd7\xa1\x96`=\xc3,\x92\xc0&<>\xce\x9ev\x875\xb2\xf8S\x9c\xde\xcfwsxU\x8c\xa9`\xca\x91\x15\xebTn\xed\xb4\xe5\xca\xfa\xfcye\xccf\xef\x9f\xcc\xc6>D\xea\x82b\x93\xb9\x9bUm\x18N\xc8\x1b\xf5\xae7)\x81\x15\x87\x10\x13\xa3\x9c\xef\x87Oot?e\xd7\xc8\xba\xbd\x17\xe7T\x86h\xfd\x9bGl\x1dN\xa5%*\xa7U\xa8\xdc\xd8\xd1\xb3\x85ZS\xf8\x81oz\xfa\xf8\xd5\xe6~Z\xb0\xbf\x02\x9aNR\x99Hp\x0b9\x97\xb4z\x93\n\x88\x92\x05w\xb9\x07\xe9L/O+o\xfe\xc1\xe3\xf3;\x1d\x98%\x93\xb1\xee#\x9f\xb40\xbb\t\xdfP\x04~F\xb5\x924\xc3\x1c\xd4\xb3\x01H\x8aB\xe1\xcc\x8a\xaa4\xea\xb5+\xe5\x9a\xf3\x0eiN\xdd\xb0\xea\x010\xa5\x86\xef\xc0\x12\xa52\x04F\x9dVc\x1325\x0cls\xcaD\xdb\x12]\xd4\xf7\xbc\xd7V\xa1\xa8?4\xe5[\xe5\x9e+O_\x84(\xf7\xf6\x84)\x12\xa3o\xf1Lp\x82\x8a\xed\xeb\x8aU\x08)?\x835\r\xf3\xf5(\x9f\xc1(SB\x02\x0c,]\x90\x9d\xf5\'\xec\xf3\x12I\x12\xd5\x0ck\xed].\xd1\xa9t\xec\xe2\xeai\xa8\xa512\xbel)\x0f\x8f\xb3\xd4-\xa2\x1b\x12u_U.!\xcbm\x04\x0bo#\xc4=UQ\n%N\x88S\x84M\x01N<\xe0|\xc4\xe0\xe1\xdd\x87\xa1\xd25O\x06@\xbaa\x90\xdf\x15u\xc6\x13\xc5\x9e\x80\xb1\xec\xbdh]S\x12\xe1Eg\\T\xc6\xf9\x9e`Z\xf9\xec\xd7\x19jXb\x83\x06G\xe2\x8dr\xe8\x11!]S\x11\x1b\xbd\xbb\x875\xdcq\xbc&/y\x12A5Q\x92\x04\x9c{\xcb\x97\xb9\x86M@\xb1Z&\xf5?f\x83\xf3d\xf5R\n\x005{\x97DO\x8a\xd2O\xeee\x06)\xbcyS\xbd,\xd2=\xde\x0c\xd7\xdf8q,f\xd9\x8f\xc0\x83q\x91\x1e\xae%\xeb\xd0\xd2IGq\xa7\xc9N\xc8k\x96\x10\xa3\x9e\x90\x01\xb5\xae:aR\xef+\xc1\x9dr\xb6gi\x15\xdc\x81t\x980\xc4\xf01,\xde\x05\x8b\xe2\xad~\xc6\x01v\xe0\x05\nVY|!\x8b\x87\xb6\x06m\xd9\x18\x82\xaa>\xc7(:rj\x18\x83\xa7~\xfd\xb2\x0e\xe6.\xf9\x84M\x86w\xad\xd2\x8cMI\xc1p\xa9\xce;\xa0\xc1w\n\xe7,\xf4\'\xd9\x9a\xd8\xed\xb1\x96$O^\xf1\xea\xb0\x06\xed\xd2\xe8-Lf\xa5?\tE7\xfc\x88\x17\xcc\x8c\x14\x0b\xb2\xb4J\xbfU\xd8\xc7c\\M\xee\xb9\x03z*\x06J0\xe2\xc0\t\x81"\x90Y\x02\xe8\xcb\x98\xbaA3;\xfe\xc31|\xfc\xc8\x03bB\xa2\xf7\x1c\xd9\x00,\xb5\x1e\xf9\x98\x06\xd46\x16,\x9c\x03\xd9\x03,\x82A_\xdb\xda\xe6\x01\xb6\x11<\x1b\xda\x18\x14\xd3\xb4\x89\x98\xb5\x13\xce^A\x9e:l^%Z\x10\x9d\xa2)SF\x13\x15P\xa0\x08\\\xf7\x16\xeb #\xf9\x941\x94\x97j\xcc\xdd\xfa\xdd\x04\x0b\x85\xfb\x93 +\xfd\xc0]^3\xd8\xc3\xc7]!H\x8cFPA\r\xbe\xbf/\xf0\x01\xb7\xea\xe6\x99\x17\x14{<\xbc\xb5R\xe1p\x7f0b\xca\xba%"q\xf3\x85U\xe6+\x1co\xf1\xc9\x04[\x08\xa7\xb1\x17\x1e \r\xec\xb6\xb7\x94;\xdc\x9e,\xf0i;q\x06\xdb\xc5-UFixPO2Et\xeb}F\x97\\\xc9`\xc3\\#\x91\x88k\x1f\x81\xb6\x8f\xd9\xc7!\xafy\xb87O1@\x00\x13Q}\xa5<o\x1c\x97x(\xb1\xaa\xa8\xee\x0e\xc4\xd0>q\xe6\x92G\xf95\xc2#\xe0\xb8\xa1\xe5$\xeaL2\x95c>f\xfd4yWR\xc5\x81l\x1d\x8a\x07\xbcG=\xc1\x16|\xb1\xa3\xac\xac\xf8\x8c\xaad\xc4\xb3\xab\xdb\x9e\xfaP\'`\x8e\xd2F\x95\x03\xd9\x87\xed\xdd\xc2\x0e6\xb1\xa7S\x97\x8b\xbe\xcc\r\x91\xf36\x85\x15\xf2\xcb\xb5+%\xd7\x8cw\xa1\x8a\x82M\xdc\x81u\x94\xdbn\x8a\x88\x06\xf4\x8b\x04av^\x01\xcf\xadwW\xee\xac\'\xcd}h\x92}\xc1*x=\x98\x18o\xb5\xabW\xc2\xedS\x01/\\}\x12G\xa3\x10\xb2,\x10\xe7"\x94\'\xff\xed\xcb=Y)\x07\xe1[\xd9Z\xd7\xec\xbb\x8c\xa2)`\xbep\xfd\x99\xf6\x1b?hy\x8d\x94\x85P\x8c\x0e\xc4\xf3\x9b\xc6\x99\xb84\xc9\xabu\xb6v\xa5\xa2\xfe*zTD\xcf\x19\x03\x1b~eM\x02!7\x9b\xbe\x99\xc8\xca\x9e\\S\xe6\xc7\x9d\xeb\xe4\xf1h\xad\\t\x92m\x14G\xe0\xadf\xf9\x89-1ig\x0cj\x8f\xb7F\xf3\\\x89\x00qqPs\x95x~\xc7\xd4\x86\x80G\xce6\x1f2s\xb9t\xc4\x9cZ+m\xa7<J\xa7\xe4L\xb3\xdew x\xc2\xeb\xc5Wa\x12\rc\x82^\xb6-\xde\xac\x862\xbc\'\x9f\xb3\xbb\xfc\x01N\x00\x15;L\x8d\xc7\x96//\xb8,N\xa8\xa9\xeb3\xc7\x89\xc6\x8e\x93\xdc\xdbl\xd9\x85\x98U\xcfW<\xb9#\xcf\xe4.-\x17f\x84;\xc3\xab\xc7n\x02N\xb0@\t\xfc<$\xc9\xab\x19zh{\x8f\x8c\xdc/\x14s(sy\x9f\xcb!\xcb\xa4\xc5c\xa9\x1e_\xa1N\x97]!\xca\xa6\t\xcd\xf7\x07Z\x82\xc6\xe9\xac\xdfc\xe6\x14\xeb]\x9b\xe2\x88+\x98\xfe#~8\x87\xf1a\xea-\xf9\xd818Q\xc9\x82~qh\xcf\xb7\x985\x968!\x12\xed0\xee\x978\x1c\xf0~\xe2\xeb\x17\xdfC\xe4\xe0\xd2]\xb8}Q\xbe\xa80~y\x90t\xd3}0\xaax\xdc\x0c\xdb\x0bO\xca\x88\r\xae\x95\x16+N^\x1fb.\xa3t{\x92@;y\xc7)\x17\'/\xb8\xe0=\x11^KO\xc6\xc4\xf2W\xf6\xca\x17j0\xd1\xac\xd0\xe5\x1coe\x06w\x9e\x1b\x9dOnOZ\xd5k\xa7\\\xe7^\xbd#C\x96J\xa70\xf0;E\x04{\x92!\x1e{;\xf4\xb6\x1d\x1c\xe4\xb2\x9f\xb8\n\x99)\xc8\xef\xfca\'g^~qn\xf2eT\xf0K\xcf}TW{\x97\r\xb7\xf3\x9dC\x82\xa6a\xc0[\x86\xd8r\xca\x9e\xd4\x8e\xadK=%\xd8JU:\xf1\xfd\xc4\xe5)d\x1d\x10\xb8\xbd\x92z\xed\xc6\xd7\x05\xce\x99\x94\x90OAF\xdfP\x12\xb5w\x07\xc1\xf3\x8f\xec\x93\x8ccS\x86^\xa9\x0e\x80\x9cS\xf5CO\xbd\xb8\x1a >\x9bO\x9d\x03\xb4\xf6\xb6\xdc\xa6\x8b\x1b)\x01N"\xa5\xa8"\xf4Tp\xd5X\xbeB\xe6\xf6(\x9e&\xf7\x01\x11B\xdb\x8c(-bO\x8e\x04\r\x1b3S\xd5/\x1b\xd4\x97\x8b^\x9e\xb5N\xe7\x88\x83\xf5\x08.X{+\xc75\x90\xe5X\x12\x85)\xa77\xcc\x07\xfc\xb0;z\xae\xb9\x0fW\x9a\xad\xbc\xee\xbb\x0e\xd8}\x9b\x13u\x89\xb9\xc2\x9e\xb1S\x07\xee\x8d-\xc7_\x88\xc0\xc6\xae\xfa\xbeP\xe6\n!\xde& \x1d\xd0\x0c\x181\xee\x9dL\xa5\x9073\xbbI\xd2\x9d\xd3\xad\x1f\xf2\x05\xc4^\n:\x7fs\x07\x9e\xff?6\n\xf7\x06\x1e\x0b_\xa7?\xdc\xafL\xfb\x05~\xdd\xf0U\x8es\x0e\x17\x1f\xe6\xdb\x0c\xff;\xf8\xe7\xbf\x01\xc8k\x8c\xb6').decode()


class Server:
    def __init__(self, host='localhost', port=25565, username='', timeout=5, quiet=True):
        # Init the hostname, port, timeout, username, etc
        self._host = host
        self._port = port
        self._username = username
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
        3: login (play)             in      ADD DESCRIPTION
        4: custom payload           in      ADD DESCRIPTION
        5: ADD MORE PACKETS
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

            play_user_id, play_hardcore, gamemode, prevous_gamemode, dimentions, rest_of_data = self.decode_packet[0x26](self.read_fully(connection)) # find out why prevous_gamemode is allways b'\xFF' and what it means
            
            if gamemode == b'\x00':
                gamemode = "survival"
            elif gamemode == b'\x01':
                gamemode = "creative"
            elif gamemode == b'\x02':
                gamemode = "adventure"
            elif gamemode == b'\x03':
                gamemode = "spectator"

            print(f"login (play): \n\tplayer EID: {play_user_id}\n\thardcore: {play_hardcore}\n\tgamemode: {gamemode}\n\tprevious gamemode: {prevous_gamemode}\n\tdimentions: {dimentions}\nextra/not unpacked: {rest_of_data}")  # Login (play), still wip as its massive
            
            print(f"Custom payload: \n\tserver flavor: {self.decode_packet['custom payload'](self.read_fully(connection))}")  # custom payload, might only work on non-pure vanilla servers
            print(f"something: {self.read_fully(connection)}")  # don't know yet

    def get_status(self, quiet=True):  # Gets a minecraft servers status, is fully compleated
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

    def honey(serveraddr=socket.gethostbyname(socket.gethostname()), serverport=25565):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.bind((serveraddr, serverport))
            server.listen(10)
            working = True
            print("started honeypot")
            while working:
                try:
                    client, addr = server.accept()

                    print(f"{addr} connected")
            
                    version, is_ping = _Packets.client.handshake(self.read_fully(client))
            
                    if is_ping:
                        print(f"{addr}: request, ping")
                        
                        self.read_fully()  # empty packet
                        data = json.dumps(pingdata).encode()
                        length = _static_pack_varint(len(data))
                        
                        client.send(b"\x00" + length + data)
            
                        data = self.read_fully(client)  # ping
                        client.send(b"\x01" + data)  # pong
                        print(f"{addr}: disconnected\n")
                        client.close()
            
                    else:
                        print(f"{addr}: request, login")
                        
                        if version > 1528:  # they are a higher version
                            client.send(_Packets.client.disconnect("outdated server! I'm still on 1.19.2."))
                            print(f"{addr}: responce, outdated server")
                            print(f"{addr}: disconnected\n")
                            client.close()
                            
                        elif version < 1528:  # they are outdated
                            client.send(_Packets.client.disconnect("outdated client! I'm on version 1.19.2"))
                            print(f"{addr}: responce, outdated client")
                            print(f"{addr}: disconnected\n")
                            client.close()
                            
                        else: # they are the same version and attempting to connect
                            print(f"\n{addr}: data, {_Packets.Client.loginstart(self.read_fully(client))}\n")  # just id data (like username, uuid, etc)
                            
                            # skipping encryption request, idk how to work mc's auth servers, but maby you can add this
                            
                            # skipping compression, because we only need to send one more packet and don't start Play mode
                            client.send(_Packets.client.disconnect("Invalid encryption response!"))
                            print(f"{addr}: disconnected\n")
                            client.close()
                except KeyboardInterrupt: 
                    working = False
                    print("finishing last client before exiting")
                    
                except Exception as err:
                    print(f"\nError encountered, continuing\nError: {err}\n")

if '__main__' == __name__:
    stat = Server()
    print(stat.honey())
