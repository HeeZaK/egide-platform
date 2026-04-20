from __future__ import annotations

import base64
import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def decode_aes256_key_b64(b64: str | None) -> bytes | None:
    """Return 32-byte key from base64, or None if unset."""
    if b64 is None or not str(b64).strip():
        return None
    raw = base64.b64decode(str(b64).strip(), validate=True)
    if len(raw) != 32:
        raise ValueError("EGIDE_FIELD_ENCRYPTION_KEY_B64 must decode to exactly 32 bytes")
    return raw


class FieldEncryptor:
    """
    AES-256-GCM for sensitive field blobs at rest (nonce prepended to ciphertext).

    Key must be exactly 32 bytes (256 bits).
    """

    _NONCE_LEN = 12

    def __init__(self, key: bytes) -> None:
        if len(key) != 32:
            raise ValueError("AES-256 requires a 32-byte key")
        self._aesgcm = AESGCM(key)

    def encrypt_to_b64(self, plaintext: bytes) -> str:
        nonce = os.urandom(self._NONCE_LEN)
        ciphertext = self._aesgcm.encrypt(nonce, plaintext, associated_data=None)
        return base64.b64encode(nonce + ciphertext).decode("ascii")

    def decrypt_from_b64(self, payload_b64: str) -> bytes:
        raw = base64.b64decode(payload_b64.encode("ascii"), validate=True)
        if len(raw) < self._NONCE_LEN + 16:
            raise ValueError("Invalid encrypted payload")
        nonce, ciphertext = raw[: self._NONCE_LEN], raw[self._NONCE_LEN :]
        return self._aesgcm.decrypt(nonce, ciphertext, associated_data=None)
