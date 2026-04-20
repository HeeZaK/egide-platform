import base64

import pytest

from app.core.crypto import FieldEncryptor, decode_aes256_key_b64


def test_decode_aes256_key_b64_roundtrip() -> None:
    key = b"k" * 32
    b64 = base64.b64encode(key).decode("ascii")
    assert decode_aes256_key_b64(b64) == key


def test_decode_aes256_key_b64_wrong_length() -> None:
    with pytest.raises(ValueError):
        decode_aes256_key_b64(base64.b64encode(b"x" * 31).decode("ascii"))


def test_field_encryptor_roundtrip() -> None:
    enc = FieldEncryptor(b"0" * 32)
    msg = b'{"secret":"value"}'
    blob = enc.encrypt_to_b64(msg)
    assert enc.decrypt_from_b64(blob) == msg
