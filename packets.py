import struct

# packet data, unpacking, packing, and simplifier (for debugging)
# obviously not done

"""
format:
ClientBound or ServerBound (to client or to server)
id number (in hex because that's how it is in https://wiki.vg

 
"""

def EXAMPLEdecode0x01(packet):  # this might not be what its like when finished
    data = struct.unpack('idddh', packet) # 
    print(f"""in: 0x01: "Spawn XP Orb"
Entity ID: {data[0]}
Cords: X: {data[1]} Y: {data[2]} Z: {data{3}}
Amount of XP: {data[4]}
""")
    return None  # will not display so we dont need to return anything

packets = {
    "ClientBound": {
        0x00: {
            "Name": "Spawn Entity",
            "Description": "Sent when a vehicle or other non-living entity is created",
            "Order": ['varint', 'uuid', 'varint', 'double', 'double', 'double', 'double', 'angle', 'angle', 'int', 'short', 'short', 'short'],
            "Order Description": ['Entity ID', 'Entity UUID', 'type of entity', 'entity X', 'entity Y', 'entity Z', 'Pitch', 'Yaw', 'Object Data', 'Velocity X', 'Velocity Y', 'Velocity Z']  # Velocity XYZ might not show up depending on the Object Data
        },
        0x01: {
            "Name": "Spawn XP Orb",
            "Description": "Spawns one or more XP orbs",
            "Order": ['varint', 'double', 'double', 'double', 'short'],
            "Order Description": ['Entity ID', 'entity X', 'entity Y', 'entity Z', 'XP rewarded when collected'],
            "Decode": EXAMPLEdecode0x01  # fix with non example
        },
        0x02: {
            "Name": "Spawn Living Entity",
            "Description": "Sent when a living entity is spawned",
            "Order": ['varint', 'uuid', 'varint', 'double', 'double', 'double', 'double', 'angle', 'angle', 'angle', 'int', 'short', 'short', 'short'],
            "Order Description": ['Entity ID', 'Entity UUID', 'type of entity', 'entity X', 'entity Y', 'entity Z', 'entity Pitch', 'entity Yaw', 'entity\'s head yaw', 'Object Data', 'Velocity X', 'Velocity Y', 'Velocity Z']
        },
        0x03: {
            "Name": "Spawn Painting",
            "Description": "Location, name, and type of a painting",
            "Order": ['varint', 'uuid', 'varint', 'position', 'Byte'],
            "Order Description": ['Entity ID', 'Entity UUID', 'Paintings ID (0-25)', 'center coordinates', 'painting direction (South: 0, West: 1, North: 2, East: 3']
        },
        0x04: {
            "Name": "Spawn Player",
            "Description": "Sent after a player enters visible range, sent after player info",
            "Order": ['varint', 'uuid', 'double', 'double', 'double', 'angle', 'angle'],
            "Order Description": ['Players Entity ID', 'Players UUID', 'Player X', 'Player Y', 'Player Z', 'Yaw', 'Pitch']
        },
        0x05: {
            "Name": "Sculk Vibration Signal",
            "Description": "None",
            "Order": ['position', 'Identifier', 'vars', 'varint'],
            "Order Description": ['Source position of vibration', 'id of codec type (?)', 'TODO', 'Ticks until vibration arrival']
        },
        0x06: {
            "Name": "Entity Animation",
            "Description": "sent when an entity changes animation",
            "Order": ['varint', 'unsigned byte'],
            "Order Description": ['Entity ID', 'Animation ID (0 swing main arm, 1 Take dmg, 2 Leave bed, 3 Swing offhand, 4 Crit effect, 5 magic crit effect)']
        },
        0x07: {
            "Name": "Statistics",
            "Description": "Response to ServerBound 0x04 'Client status'",
            "Order": ['varint', ['varint', 'varint', 'varint']],  # a sub list means an array that contains the types
            "Order Description": ['number of elements in fallowing array', ['varries', 'varries', 'value to set to']]
        },
        0x08: {
            "Name": "Acknowledge Player Digging",
            "Descripton": "confims that the player is digging",
            "Order": ['postion', 'varint', 'varint', 'bool'],
            "Order Description": ['postion of digging', 'block state ID of the block that should be at the postion of digging', '0 Started digging, 1 Cancelled digging, 2 finished digging']
        },
        0x09: {
            "Name": "Block Break Animation",
            "Descripton": "Destroy stages of a block getting dug",
            "Order": ['varint', 'postion', 'byte'],
            "Order Description": ['Entity ID', 'Postion where to display', 'Destroy stage 0-9, any other removes it']
        },
        0x0A: {
            "Name": "Block Entity Data",
            "Description": "Sets block entity associated with block at given location",
            "Order": ['postion', 'varint', 'NBT'],
            "Order Description": ['location of block', 'type of block entity', 'Data to set (as NBT tag)']
        },
        0x0B: {
            "Name": "Block Action",
            "Description": "block actions and animations",
            "Order": ['postion', 'unsigned byte', 'unsigned byte', 'varint'],
            "Order Description": ['Block Cordients', 'Varries on block', 'varries on block', 'block type ID']
        }
    }, # add more packets
    "SeverBound": {
        # add  packets
        }
    }
}

