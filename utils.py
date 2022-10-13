import socket
import templates
from datatypes import VarInt, String
import zlib


def get_packet(sock):
    raw_buffer = b""
    raw_buffer += sock.recv(1)
    if raw_buffer:
        while raw_buffer[-1] > 127:
            raw_buffer += sock.recv(1)
    else:
        raise Exception("get_packet disconnected while getting initial buffer")

    buffer = VarInt().decode(raw_buffer)[0]
    rawPacket = b""
    while len(rawPacket) < buffer:
        data = sock.recv(buffer - len(rawPacket))
        if data:
            rawPacket += data
        else:
            raise Exception("socket disconnected while reading packet")

    return raw_buffer + rawPacket


def frame_pack(packet, compression_level):
    if compression_level >= 0:
        packet_length = len(packet)
        if packet_length > compression_level:
            packet = VarInt().encode(packet_length) + zlib.compress(packet)
        else:
            packet = b"\x00" + packet
    return String().encode(packet)


def frame_unpack(frame, compression_level):
    bufferless_frame = String().decode(frame)[0]
    if compression_level >= 0:
        packet_length, buffer_length = VarInt().decode(bufferless_frame)
        if packet_length > 0:
            packet = zlib.decompress(bufferless_frame[buffer_length:])
        else:
            packet = bufferless_frame[buffer_length:]
    else:
        packet = bufferless_frame
    return packet


def template_select(headers, bound_to, packet_id):
    for template in templates.templates:

        # check if template headers match
        if (template["HEADER"]["BoundTo"], template["HEADER"]["State"],
                template["HEADER"]["PacketId"]) == (bound_to, headers["State"], packet_id):
            if (headers["ProtocolVersion"] in template["HEADER"]
                    ["ProtocolVersion"] or not template["HEADER"]["ProtocolVersion"]):
                return template
    return {
        "TAG": "unknown",
        "HEADER": {
            "ProtocolVersion": [],
            "BoundTo": bound_to,
            "State": headers["State"],
            "PacketId": packet_id
        }, "PAYLOAD": {}
    }

    print(f"template_select didnt find {bound_to, headers['State'],packed_id}")


def packet_parse(raw_packet, template):
    packet_id, packet_id_length = VarInt().decode(raw_packet)
    raw_packet = raw_packet[packet_id_length:]

    packet = {}

    if not template:
        return {
            "tag": "unknown",
            "PAYLOAD": {
                "unknown": raw_packet
            }
        }
    for i in template["PAYLOAD"]:
        packet[i], _ = template["PAYLOAD"][i].decode(raw_packet)
        raw_packet = raw_packet[_:]

    packet["HEADER"] = template["HEADER"]
    packet["unknown"] = raw_packet
    return packet


def packet_build(template, packet):
    # complain if user forgot payload args
    missing = [i for i in list(template["PAYLOAD"]) if i not in packet]
    if missing:
        raise Exception(f"{template['HEADER']} requires {missing}")

    # construct from template
    raw_packet = b""
    raw_packet += VarInt().encode(packet["HEADER"]["PacketId"])
    for variable in template["PAYLOAD"]:
        raw_packet += template["PAYLOAD"][variable].encode(packet[variable])

    raw_packet += packet["unknown"]
    return raw_packet
