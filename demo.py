import socket
import _thread
from datatypes import VarInt
from utils import packet_parse, packet_build, template_select, frame_unpack, frame_pack, get_packet
from plugins import state_update, compression_update, listen_chat

target = ("localhost", 25565)
proxy = ("localhost", 8888)


def pipe(insock, outsock, headers, bound_to):
    "the connection between client and server"
    while True:
        packet_frame = get_packet(insock)
        raw_packet = frame_unpack(packet_frame, headers["Compression"])

        template = template_select(
            headers, bound_to, VarInt().decode(raw_packet)[0])

        packet = packet_parse(raw_packet, template)
        listen_chat(headers, bound_to, packet)
        raw_packet = packet_build(template, packet)

        packet_frame = frame_pack(raw_packet, headers["Compression"])

        compression_update(headers, bound_to, packet)

        state_update(headers, bound_to, packet)
        outsock.send(packet_frame)


def main():
    "simple proxy demo, replays chat, and join messages."
    server = socket.create_server(proxy)
    while True:
        inbound, _ = server.accept()
        outbound = socket.create_connection(target)

        headers = {
            "Compression": -1,
            "ProtocolVersion": 0,
            "State": "Handshaking"
        }
        _thread.start_new(pipe, (inbound, outbound, headers, "Server"))
        _thread.start_new(pipe, (outbound, inbound, headers, "Client"))


if __name__ == "__main__":
    main()
