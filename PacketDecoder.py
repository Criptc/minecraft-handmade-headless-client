import uuid
import struct
import json


def _static_pack_varint(val):
	total = b''
	if val < 0:
		val = (1<<32)+val
	while val>=0x80:
		bits = val&0x7F
		val >>= 7
		total += struct.pack('B', (0x80|bits))
	bits = val&0x7F
	total += struct.pack('B', bits)
	return total


def _static_unpack_varint(data, return_num=False):
    total = 0
    shift = 0
    val = 0x80
    n = 0
    while val & 0x80:
        val = struct.unpack('B', data[n:n+1])[0]
        total |= ((val & 0x7F) << shift)
        shift += 7
        n += 1
    if total & (1 << 31):
        total = total - (1 << 32)
    if return_num:
        return total, n
    else:
        return total


class _Packets:
    class Tools:
        @staticmethod
        def decode_uuid(data_packet):
            if len(data_packet) > 16:
                data = data_packet[0:16]
            else:
                data = data_packet

            print(len(data))
            data = uuid.UUID(bytes=data)
            uuid_data = data.hex
            # a minecraft uuid is 8-4-4-4-12
            uuid_out = f"{uuid_data[0:8]}-{uuid_data[9:13]}-{uuid_data[14:18]}-{uuid_data[19:23]}-{uuid_data[23:45]}"
            packet_leftover = data_packet[16:len(data_packet)]
            return uuid_out, packet_leftover

    class Decode:
        @staticmethod
        def login_0x02(data_packet):
            login_uuid, login_suc_bytes = _Packets.Tools.decode_uuid(data_packet)
            login_suc_bytes = login_suc_bytes[1:len(login_suc_bytes)]
            username = []
            for i in range(len(login_suc_bytes)):
                try:
                    if login_suc_bytes[i:i+1].decode().isprintable():
                        username.append(login_suc_bytes[i:i+1].decode())
                    else:
                        break
                except Exception:
                    pass
            return login_uuid, ''.join(username), login_suc_bytes

        @staticmethod
        def login_0x03(data_packet):
            return _static_unpack_varint(data_packet)
        
        @staticmethod
        def play_0x26(data_packet):
            print(data_packet[0:20])
            print('\n')
            out = []
            data = struct.unpack_from('i?Bc', data_packet)
            for i in data:
                out.append(i)
            rest = data_packet[8:len(data_packet)]  # would be 7, but there is a random \xff in there
            dimention = _static_unpack_varint(rest)
            rest = rest[1:len(rest)]
            dimentions = []
            
            for i in range(dimention):
                length = _static_unpack_varint(rest)
                rest = rest[1:len(rest)]
                mid = ''
                data = struct.unpack_from('c'*length, rest)
                
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
    class client:
        @staticmethod
        def handshake(packet_data):
            protocol_version, n = _static_unpack_varint(packet_data, return_num=True)
            packet_data = packet_data[n:len(packet_data)]
            if packet_data.endswith(b'\x01'):
                return protocol_version, False
            else:
                return protocol_version, True

        @staticmethod
        def loginstart(packet_data):
            username = []
            for i in range(len(packet_data)):
                try:
                    if packet_data[i:i+1].decode().isprintable():
                        username.append(packet_data[i:i+1].decode())
                    else:
                        break
                except:
                    pass
            username = "".join(username)
            packet_data = packet_data[len(username):len(packet_data)]
            sig_data = struct.unpack_from('?', packet_data)
            packet_data = packet_data[1:len(packet_data)]
            if sig_data:
                timestamp = struct.unpack_from('l', packet_data)
                length = len(struct.pack('l', timestamp))
                packet_data = packet_data[length:len(packet_data)]
                pubkeylen, n = _static_unpack_varint(packet_data, return_num=True)
                packet_data = packet_data[1:len(packet_data)]
                pubkey = struct.unpack_from('c'*pubkeylen, packet_data)
                packet_data = packet_data[pubkeylen:len(packet_data)]
                signiturelen, n = _static_unpack_varint(packet_data, return_num=True)
                packet_data = packet_data[1:len(packet_data)]
                signiture = struct.unpack_from('c'*signiturelen, packet_data)
                packet_data = packet_data[signiturelen:len(packet_data)]

            hasUUID = struct.unpack_from('?', packet_data)
            if hasUUID:
                packet_data = packet_data[1:len(packet_data)]
                puuid = _Packets.Tools.decode_uuid(packet_data)

            if sig_data:
                if hasUUID:
                    return {"username": username, "sigdata": True, "timestamp": timestamp, "publickey": pubkey, "signiture": signiture, "hasUUID": True, "UUID": puuid}
                else:
                    return {"username": username, "sigdata": True, "timestamp": timestamp, "publickey": pubkey, "signiture": signiture, "hasUUID": False}
            else:
                if hasUUID:
                    return {"username": username, "sigdata": False, "hasUUID": True, "UUID": puuid}
                else:
                    return {"username": username, "sigdata": False, "hasUUID": False}

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

            packet += json.dumps(json_data)
            packet = _static_pack_varint(len(packet)) + packet
            return packet
            
                
packet = {
    "decode": {
        "login": {
            0x02: _Packets.Decode.login_0x02,
            0x03: _Packets.Decode.login_0x03
        },
        "play": {
            "custom payload": _Packets.Special.custom_payload,
            0x26: _Packets.Decode.play_0x26
        }
    },
    "encode": {

    }
}
