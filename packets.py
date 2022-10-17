# packet data, unpacking, packing, and simplifier (for debugging)
# obviously not done

"""
format:
ClientBound or ServerBound (to client or to server)
id number (in hex because that's how it is in https://wiki.vg

"""

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
            "Order Description": ['Entity ID', 'entity X', 'entity Y', 'entity Z', 'XP rewarded when collected']
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
        }
    }
}
