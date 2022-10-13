
def state_update(headers, bound_to, packet):
    "updates the header's State."
    if (bound_to, headers["State"], packet["HEADER"]["PacketId"]) == ("Server", "Handshaking", 0):
        if packet["NextState"] == 1:
            headers["State"] = "Status"
            print("state set Status")
        if packet["NextState"] == 2:
            headers["State"] = "Login"
            print("state set Login")

    if (bound_to, headers["State"], packet["HEADER"]["PacketId"]) == ("Client", "Login", 2):
        headers["State"] = "Play"
        headers["Username"] = packet["Username"]
        print(headers["Username"], "state set to play")


def compression_update(headers, bound_to, packet):
    "detects set compression packet and tell's frame_pack/frame_unpack to compress and decompress."
    if (bound_to, headers["State"], packet["HEADER"]["PacketId"]) == ("Client", "Login", 3):
        headers["Compression"] = packet["Threshold"]
        print("set compression", packet["Threshold"])


def listen_chat(headers, bound_to, packet):
    "prints player chat"
    if (bound_to, headers["State"], packet["HEADER"]["PacketId"]) == ("Server", "Play", 3):
        print(headers["Username"].decode(), packet["Message"].decode())


