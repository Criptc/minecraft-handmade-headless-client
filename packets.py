# packet data, unpacking, packing, and simplifier (for debugging)
# obviously not done

packets = {
    "ClientBound": {
        b'\x00': {
            "Name": "Spawn Entity",
            "Order": ['varint']
        }
    }
}
