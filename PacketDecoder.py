import uuid
import struct


def _static_unpack_varint(data):
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
    return total


class _Packets:
    class Tools:
        @staticmethod
        def decode_uuid(data_packet):
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
        def login_0x02(data_packet):
            login_uuid, login_suc_bytes = _Packets.Tools.decode_uuid(data_packet)
            login_suc_bytes = login_suc_bytes[1:len(login_suc_bytes)]
            username = []
            for i in range(len(login_suc_bytes)):
                try:
                    if login_suc_bytes[i:i+1].decode().isprintable():
                        username.append(login_suc_bytes[i:i+1].decode())
                    else:
                        print(i)
                        break
                except Exception:
                    pass
            return login_uuid, ''.join(username), login_suc_bytes

        @staticmethod
        def play_0x26(data_packet):
            out = []
            data = struct.unpack_from('i?cc', data_packet)
            for i in data:
                out.append(i)
            rest = data_packet[8:len(data_packet)]
            out.append(_static_unpack_varint(rest))
            out.append(rest[1:len(rest)])
            return out

    class Special:
        @staticmethod
        def custom_payload(packet_data):
            packet_data = packet_data[16:len(packet_data)]
            server_type = []

            for i in range(len(packet_data)):
                try:
                    if packet_data[i:i+1].decode().isprintable():
                        server_type.append(packet_data[i:i+1].decode())
                    else:
                        print(i)
                        break
                except Exception:
                    pass
            return ''.join(server_type)


packet = {
    "decode": {
        "login": {
            0x02: _Packets.Decode.login_0x02
        },
        "play": {
            "custom payload": _Packets.Special.custom_payload,
            0x26: _Packets.Decode.play_0x26
        }
    },
    "encode": {

    }
}
