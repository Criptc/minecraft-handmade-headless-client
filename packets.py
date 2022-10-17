import struct

# packet data, unpacking, packing, and simplifier (for debugging)
# obviously not done

"""
format: only here because i dont like writing it every time

            "Name": "",
            "Description": "",
            "Order": [''],
            "Order Description": ['']
"""


def EXAMPLEdecode0x01(packet):  # this might not be what its like when finished
    data = struct.unpack('idddh', packet)
    print(f"""in: 0x01: "Spawn XP Orb"
Entity ID: {data[0]}
Cords: X: {data[1]} Y: {data[2]} Z: {data[3]}
Amount of XP: {data[4]}
""")
    return None  # will not display, so we don't need to return anything


types = {  # None means add later
    "uuid": None,
    "angle": None,
    "title": None,
    "slot": None,
    "chat": "json"  # chat is just a certain format of json
}

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
            "Description": "None(?)",
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
            "Order Description": ['number of elements in fallowing array', ['varies', 'varies', 'value to set to']]
        },
        0x08: {
            "Name": "Acknowledge Player Digging",
            "Description": "configs that the player is digging",
            "Order": ['position', 'varint', 'varint', 'bool'],
            "Order Description": ['position of digging', 'block state ID of the block that should be at the position of digging', '0 Started digging, 1 Cancelled digging, 2 finished digging']
        },
        0x09: {
            "Name": "Block Break Animation",
            "Description": "Destroy stages of a block getting dug",
            "Order": ['varint', 'position', 'byte'],
            "Order Description": ['Entity ID', 'Position where to display', 'Destroy stage 0-9, any other removes it']
        },
        0x0A: {
            "Name": "Block Entity Data",
            "Description": "Sets block entity associated with block at given location",
            "Order": ['position', 'varint', 'NBT'],
            "Order Description": ['location of block', 'type of block entity', 'Data to set (as NBT tag)']
        },
        0x0B: {
            "Name": "Block Action",
            "Description": "block actions and animations",
            "Order": ['position', 'unsigned byte', 'unsigned byte', 'varint'],
            "Order Description": ['Block Coordinates', 'Varies on block', 'varies on block', 'block type ID']
        },
        0x0C: {
            "Name": "Block Change",
            "Description": "send when a block is changed within view distance",
            "Order": ['position', 'varint'],
            "Order Description": ['location of the block that gets changed', 'The new block state ID ']
        },
        0x0D: {
            "Name": "Boss Bar",
            "Description": "shows a boss bar",
            "Order": ['uuid', 'varint', {0: [types['chat'], 'float', 'varint', 'varint', 'unsigned byte'], 1: None, 2: 'float', 3: types['chat'], 4: ['varint', 'varint'], 5: 'unsigned byte'}],
            "Order Description": ['UUID for the bar', 'Layout of next section', {0: ['title of the boss bar', 'color ID', 'Type of division', 'Bitmask (aka flags)'], 1: 'removes the boss bare', 2: 'updates the heath to number', 3: 'update title', 4: ['Color ID', 'Dividers'], 5: 'update flags'}]
        },
        0x0E: {
            "Name": "Server Difficulty",
            "Description": "changes the clients difficulty setting in the option menu",
            "Order": ['unsigned byte', 'bool'],
            "Order Description": [{0: 'peaceful', 1: 'easy', 2: 'normal', 3: 'hard'}, 'is the difficulty locked']
        },
        0x0F: {
            "Name": "Chat message",
            "Description": "sent to display a chat message",
            "Order": [types['chat'], 'byte', 'uuid'],
            "Order Description": ['chat message to display', {0: 'normal message (chat box)', 1: 'system message (chat box)', 2: 'game info (above chat bar)'}, 'uuid of sender (?)']
        },
        0x10: {
            "Name": "Clear titles",
            "Description": "clears current title info with option to reset it",
            "Order": ['bool'],
            "Order Description": ['weather to reset title info (true) or just remove it (false)']
        },
        0x11: {
            "Name": "Tab-Complete",
            "Description": "list of auto completes for command names, parameters, and usernames",
            "Order": ['varint', 'varint', 'varint', 'varint', 'string', 'bool', types['chat']],
            "Order Description": ['Transaction ID', 'Start of text to replace', 'end of text to replace', 'number of elements in fallowing array (string?)', 'string', 'True if fallowing is present else, false', 'tool tip to display']
        },
        0x12: {
            "Name": "Declare Commands",
            "Description": "list of commands on the server and how they are parsed",
            "Order": ['varint', 'nodes (?)', 'varint'],
            "Order Description": ['number of elements in fallowing array', 'array of nodes', 'index of root node in previous array']
        },
        0x13: {
            "Name": "Close Window",
            "Description": "sent when a window is force closed",
            "Order": ['unsigned byte'],
            "Order Description": ['id of window closed']
        },
        0x14: {
            "Name": "Window Items",
            "Description": "sent when multiple window items are removed or added including armors",
            "Order": ['unsigned byte', 'varint', 'varint', 'array of slot(?)', 'slot(?)'],
            "Order Description": ['ID of window changing', 'State ID', 'num of elements in fallowing array', 'array of slots(?)', 'item held by player']
        },
        0x15: {
            "Name": "Window Property",
            "Description": "sent when part of a gui window should change (or update)",
            "Order": ['unsigned byte', 'short', 'short'],
            "Order Description": ['Window ID', 'Property to be updated', 'new value for the property']
        },
        0x16: {
            "Name": "Set Slot",
            "Description": "sent when a single item is removed or added to a slot in a window",
            "Order": ['byte', 'varint', 'short', 'slot(?)'],
            "Order Description": ['window being updated', 'state ID', 'slot to be updated', 'slot data']
        },
        0x17: {
            "Name": "Set Cooldown",
            "Description": "Applies a cooldown to an item (like ender pearls)",
            "Order": ['varint', 'varint'],
            "Order Description": ['Item ID', 'cooldown ticks']
        },
        0x18: {
            "Name": "Plugin Message",
            "Description": "mods an plugins use this to send their data (some are minecraft)",
            "Order": ['identifier', 'byte array'],
            "Order Description": ['name of the plugin channel used to send data', 'data for the plugin']
        },
        0x19: {
            "Name": "Named sound effect",
            "Description": "used to play a sound effect on the client, can be custom effects from an resource pack",
            "Order": ['sound id(?)', 'varint', 'int', 'int', 'int', 'float', 'float'],
            "Order Description": ['ID of sound to play', 'category to play the sound from', 'source X', 'source Y', 'source Z', 'volume (can go above 1 aka 100%)', 'pitch (between 0.5 and 2.0)']
        },
        0x1A: {
            "Name": "Disconnect",
            "Description": "sent before the server disconnects the client",
            "Order": [types["chat"]],
            "Order Description": ['message to display on disconnect']
        },
        0x1B: {
            "Name": "Entity Status",
            "Description": "generally triggers an animation",
            "Order": ['int', 'byte'],
            "Order Description": ['Entity ID', 'Entity status']
        },
        0x1C: {
            "Name": "Explosion",
            "Description": "sent when a explosion happens",
            "Order": ['float', 'float', 'float', 'float', 'varint', 'byte array', 'float', 'float', 'float'],
            "Order Description": ['position X', 'position Y', 'position Z', 'strength of the explosion', 'records (?)', 'player velocity X', 'player velocity Y', 'player velocity Z']
        },
        0x1D: {
            "Name": "Unload chunk",
            "Description": "unloads an chunk at position",
            "Order": ['int', 'int'],
            "Order Description": ['chunk X', 'chunk Y']
        },
        0x1E: {
            "Name": "Change Game State",
            "Description": "used for a lot of game state things, ie: weather, bed use, gamemode, etc",
            "Order": ['unsigned byte', 'var'],
            "Order Description": ['Reason (effect number)', 'value for effect']
        },
        0x1F: {
            "Name": "Open Horse Window",
            "Description": "Open Window but for horses and other living mounts with chests",
            "Order": ['unsigned byte', 'varint', 'int'],
            "Order Description": ['window ID', 'slot count', 'Entity ID']
        },
        0x20: {
            "Name": "Initialize World Border",  # no-clue how it makes the border with only a single x, y, and diameter (probably just me being dumb)
            "Description": "shows the world border, border effects, and border moving",
            "Order": ['double', 'double', 'double', 'double', 'varlong(?)', 'varint', 'varint', 'varint'],
            "Order Description": ['X', 'Z', 'Old Diameter', 'New Diameter', 'milliseconds until New Diameter is reached', 'Portal Teleport Boundary', 'warning blocks (?)', 'Warning time (?)']
        },
        0x21: {
            "Name": "Keep Alive",  # HIGHLY IMPORTANT
            "Description": "Server sends out an ping with a random ID, if you dont respond with the same one, you'll get kick for timeout",
            "Order": ['long'],
            "Order Description": ['random ID']
        },
        0x22: {
            "Name": "Chunk Data And Update Light",  # wiki needs better capitalizing
            "Description": "Sends chunk data (when chunk is loaded(?)), dimension is up to client",
            "Order": ['int', 'int', 'NBT', 'varint', 'byte array', 'varint', ['byte', 'short', 'varint', 'NBT'], 'bool', 'bitset(?)', 'bitset(?)', 'bitset(?)', 'bitset(?)', 'varint', ['varint', 'bytes'], 'varint', ['varint', 'bytes']],
            "Order Description": ['Chunk X', 'Chunk Y', 'Height maps(?)', 'size of data in bytes', 'data', 'number of elements in fallowing array', ['packed section coordinates', 'y height', 'type of block entity', 'blocks entity data without position (XYZ) values'], 'if edges should be trusted for light updates(?)', '(?)', '(?)', '(?)', '(?)', 'number of elements in fallowing array (should be the same as num of bits in sky light mask)', ['length of fallowing array (why is this needed?)', 'array of bytes (for?)'], 'number of elements in fallowing array', ['length of fallowing array (why is this needed?)', 'array of bytes (for?)']]
        },
        0x23: {
            "Name": "Effect",
            "Description": "sent when a client is ment to play a sound or particle effect",
            "Order": ['int', 'position(?)', 'int', 'bool'],
            "Order Description": ['ID of effect', 'location of effect', 'extra data for certain effects', 'extra data for certain effects']
        },
        0x24: {
            "Name": "Particle",
            "Description": "displays a certain particle",
            "Order": ['int', 'bool', 'double', 'double', 'double', 'float', 'float', 'float', 'float', 'int', 'var'],
            "Order Description": ['Particle ID', 'if distance is between 256 to 65536', 'X position', 'Y position', 'Z position', 'Offset X', 'Offset Y', 'Offset Z', 'particle Data(why float?)', 'particle count', 'variable depending on on particle']
        }
    },  # add more packets
    "SeverBound": {
        0x00: {
            "Name": "Teleport Confirm",
            "Description": "sent as confirmation of Player Position And Look (add ID(?))",
            "Order": ['varint'],
            "Order Description": ['ID given by the Player Position And Look packet (add ID(?))']
        },
        0x01: {
            "Name": "Query Block NBT",
            "Description": "Used when Shift+F3+I is pressed looking at a block",
            "Order": ['varint', 'position(?)'],
            "Order Description": ['ID to varify that the response matches', 'location of the block to check']
        },
        0x02: {
            "Name": "Set Difficulty",
            "Description": "must have op level 2, only use seems to be in single player",
            "Order": ['byte'],
            "Order Description": ['new difficulty (0 peaceful, 1 easy, 2 normal, 3 hard)']
        },
        0x03: {
            "Name": "Chat Message",
            "Description": "used to send a message (cant be longer then 256(why?)) if the message starts with '/' will try to interpret it as a command",
            "Order": ['string'],
            "Order Description": ['raw message (why not types["chat"]?']
        },
        0x04: {
            "Name": "Client Status",
            "Description": "NONE(?)",
            "Order": ['varint'],
            "Order Description": ['Action ID (0 for preform respawn, 1 for Request stats)']
        },
        0x05: {
            "Name": "Client Settings",
            "Description": "sent when client connects or when settings are changed",
            "Order": ['string', 'byte', 'varint', 'bool', 'unsigned byte', 'varint', 'bool', 'bool'],
            "Order Description": ['Locale (?)', 'View Distance', 'Chat Mode', 'Chat Colors (can chat be colored)', 'Displayed Character parts (better name then skin parts)', 'Main hand', 'Enable Text Filtering', 'Allow server listings']  # Allow server listings should allow ability to hide presents on server
        },
        0x06: {
            "Name": "Tab-Complete",
            "Description": "sent when a client needs to tab-complete a suggestion type",
            "Order": ['varint', 'string'],
            "Order Description": ['Transaction ID', 'All the text behind the cursor without the "/"']
        },
        0x07: {
            "Name": "Click Window Button",
            "Description": "used when clicking on a window's button",
            "Order": ['byte', 'byte'],
            "Order Description": ['Window ID', 'Button ID']
        }
    }
}
