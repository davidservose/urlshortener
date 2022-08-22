import zlib


class Hasher:
    @staticmethod
    def hash(value: str) -> int:
        return zlib.crc32(bytes(value, "utf-8"))
