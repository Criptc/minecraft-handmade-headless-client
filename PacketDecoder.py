import uuid
import struct
import json
import base64


def _static_pack_varint(val):
    total = b''
    if val < 0:
        val = (1 << 32) + val
    while val >= 0x80:
        bits = val & 0x7F
        val >>= 7
        total += struct.pack('B', (0x80 | bits))
    bits = val & 0x7F
    total += struct.pack('B', bits)
    return total


def _static_unpack_varint(data, return_num=False):
    total = 0
    shift = 0
    val = 0x80
    n = 0
    while val & 0x80:
        val = struct.unpack('B', data[n:n + 1])[0]
        total |= ((val & 0x7F) << shift)
        shift += 7
        n += 1
    if total & (1 << 31):
        total = total - (1 << 32)
    if return_num:
        return total, n
    else:
        return total


class packets:
    class Tools:
        @staticmethod
        def decode_uuid(data_packet):
            length, n = _static_unpack_varint(data_packet, return_num=True)
            print(length, "  ", n)
            data_packet = data_packet[n:len(data_packet)]

            if len(data_packet) > 16:
                data = data_packet[0:16]
            else:
                data = data_packet

            data = uuid.UUID(bytes=data)
            uuid_data = data.hex
            # a minecraft uuid is 8-4-4-4-12
            uuid_out = f"{uuid_data[0:8]}-{uuid_data[9:13]}-{uuid_data[14:18]}-{uuid_data[19:23]}-{uuid_data[23:45]}"
            packet_leftover = data_packet[16:len(data_packet)]
            return uuid_out, packet_leftover

    class Decode:
        @staticmethod
        def login_0x01(data_packet):
            serverID_len, n = _static_unpack_varint(data_packet, return_num=True)
            data_packet = data_packet[n:len(data_packet)]

            serverID = data_packet[0:serverID_len]
            data_packet = data_packet[0:serverID_len]

            pubkeylen, n = _static_unpack_varint(data_packet, return_num=True)
            data_packet = data_packet[0:n]

            pubkey = data_packet[0:pubkeylen]
            data_packet = data_packet[0:pubkeylen]

            pubkey = base64.b64encode(pubkey)
            pubkeyout = "-----BEGIN PUBLIC KEY-----\n"

            n = 0
            for i in list(pubkey):
                if n == 64:
                    pubkeyout += '\n'
                pubkeyout += i
                n += 1

            pubkeyout += "\n-----END PUBLIC KEY-----"

            tokenlen, n = _static_unpack_varint(data_packet, return_num=True)
            data_packet = data_packet[0:n]

            token = data_packet[0:tokenlen]
            data_packet = data_packet[0:tokenlen]

            return serverID, pubkey, token

        @staticmethod
        def login_0x02(data_packet):
            login_uuid, data_packet = packets.Tools.decode_uuid(data_packet)

            print(data_packet)
            length, n = _static_unpack_varint(data_packet, return_num=True)
            data_packet = data_packet[n:len(data_packet)]
            username = data_packet[0:length].decode()

            return login_uuid, username

        @staticmethod
        def login_0x03(data_packet):
            print(data_packet)
            return _static_unpack_varint(data_packet)

        @staticmethod
        def play_0x26(data_packet):
            out = []
            print(data_packet[0:128])
            data = struct.unpack_from('i?Bc', data_packet)
            for i in data:
                out.append(i)
            rest = data_packet[8:len(data_packet)]
            dimention = _static_unpack_varint(rest)
            print("\n", rest[0:1], '\n')
            rest = rest[1:len(rest)]
            dimentions = []

            for i in range(dimention):
                length = _static_unpack_varint(rest)
                rest = rest[1:len(rest)]
                mid = ''
                data = struct.unpack_from('c' * length, rest)

                for i in data:
                    try:
                        mid += i.decode()
                    except UnicodeDecodeError:
                        print(i)

                dimentions.append(mid)
                rest = rest[length:len(rest)]

            out.append(dimentions)
            out.append(rest[0:len(rest)])
            return out

    class Special:
        @staticmethod
        def Encryption_Request(packet_data):
            packet_data = packet_data[20:len(packet_data)]
            length, num = _static_unpack_varint(packet_data, return_num=True)

        @staticmethod
        def custom_payload(packet_data):
            return packet_data

    class Client:
        @staticmethod
        def handshake(packet_data):

            protocol_version = struct.unpack_from("H", packet_data)[0]
            packet_data = packet_data[2:len(packet_data)]

            if packet_data.endswith(b'\x01'):
                return protocol_version, True
            elif packet_data.endswith(b"\x02"):
                return protocol_version, False
            else:
                return protocol_version, False

        @staticmethod
        def loginstart(packet_data):
            print(packet_data)
            length, n = _static_unpack_varint(packet_data, return_num=True)
            packet_data = packet_data[n:len(packet_data)]
            username = packet_data[0:length].decode()
            packet_data = packet_data[length:len(packet_data)]

            if packet_data != b'':
                return {"username": username, "hasUUID": False}

            hasUUID = struct.unpack_from('?', packet_data)
            if hasUUID:
                packet_data = packet_data[1:len(packet_data)]
                puuid = packets.Tools.decode_uuid(packet_data)
                return {"username": username, "hasUUID": True, "UUID": puuid}
            else:
                return {"username": username, "hasUUID": False}

        @staticmethod
        def setcompression(maxpaksize):
            return b"\x03" + _static_pack_varint(maxpaksize)

        @staticmethod
        def disconnect(reason, bold=False, italic=False, underlined=False, strikethrough=False):
            packet = b"\x00"

            json_data = {
                "text": reason,
                "bold": bold,
                "italic": italic,
                "underlined": underlined,
                "strikethrough": strikethrough
            }

            packet += json.dumps(json_data).encode()
            return packet
