import zlib


class Hasher:
    @staticmethod
    def hash(value: str) -> int:
        return zlib.adler32(bytes(value, "utf-8"))
