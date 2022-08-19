from hashing import Hasher


def test_hash():
    hashed_url = Hasher.hash("http://www.testurl.com")
    assert hashed_url is not None


def test_multiple_hash_values():
    assert Hasher.hash("value 1") != Hasher.hash("value 2")
