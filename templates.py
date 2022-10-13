from datatypes import UUID, VarInt, String, UnsignedShort

templates = [

    {
        "TAG": "compression level",
        "HEADER": {
            "ProtocolVersion": [],
            "BoundTo":"Client",
            "State": "Login",
            "PacketId":3
        },
        "PAYLOAD":{
            "Threshold": VarInt()
        }

    },
    # BoundTo Server
    {
        "TAG": "Handshake",
        "HEADER": {
            "ProtocolVersion": [],
            "BoundTo":"Server",
            "State": "Handshaking",
            "PacketId":0
        },
        "PAYLOAD":{
            "ProtocolVersion": VarInt(),
            "ServerAddress": String(),
            "ServerPort": UnsignedShort(),
            "NextState": VarInt()
        }
    },
    # Status
    {
        "TAG": "",
        "HEADER": {
            "ProtocolVersion": [],
            "BoundTo":"Server",
            "State": "Status",
            "PacketId":0
        },
        "PAYLOAD":{
        }

    },
    # Login
    {
        "TAG": "Login Start",
        "HEADER": {
            "ProtocolVersion": [],
            "BoundTo":"Server",
            "State": "Login",
            "PacketId":0
        },
        "PAYLOAD":{
            "Username": String()
        }
    },
    {
        "TAG": "Login Success",
        "HEADER": {
            "ProtocolVersion": [],
            "BoundTo":"Client",
            "State": "Login",
            "PacketId":2
        },
        "PAYLOAD":{
            "UUID": UUID(),
            "Username": String()
        }
    },


    # Play

    {
        "TAG": "chat",
        "HEADER": {
            "ProtocolVersion": [],
            "BoundTo":"Server",
            "State": "Play",
            "PacketId":3
        },
        "PAYLOAD":{
            "Message": String()
        }
    },

    # BoundTo Client
    # Handshaking (there arn't any in the main protocol)

    # Status
    {
        "TAG": "server-status",
        "HEADER": {
            "ProtocolVersion": [],
            "BoundTo":"Client",
            "State": "Status",
            "PacketId":0
        },
        "PAYLOAD":{
            "json": String()
        }
    }




]
