import struct


class UUID():
    def encode(self, Data):
        return Data

    def decode(self, Data):
        return Data[:16], 16


class String():

    def encode(self, Data):
        return VarInt().encode(len(Data)) + Data

    def decode(self, Data):
        _ = VarInt().decode(Data)
        p = sum(_)
        return Data[_[1]:p], p


class UnsignedShort():
    def encode(self, Data):
        return struct.pack(">H", Data)

    def decode(self, Data):
        return struct.unpack(">H", Data[:2])[0], 2


class VarInt():
    def decode(self, data):
        d, l = 0, 0
        length = len(data)
        if length > 5:
            length = 5
        for i in range(length):
            l += 1
            b = data[i]
            d |= (b & 0x7F) << 7 * i
            if not b & 0x80:
                break
        return d, l

    def encode(self, d):
        o = b''
        while True:
            b = d & 0x7F
            d >>= 7
            o += struct.pack("B", b | (0x80 if d > 0 else 0))
            if d == 0:
                break
        return o
