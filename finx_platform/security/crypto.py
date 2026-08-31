"""Sensitive Data Masking and Symmetric Encryption Helpers."""

import base64
import hashlib


def mask_pan(pan_number: str) -> str:
    """Masks PAN: ABCDE1234F -> ABCDE****F"""
    if not pan_number or len(pan_number) < 6:
        return "******"
    return pan_number[:5] + "****" + pan_number[-1:]


def mask_card_number(card_number: str) -> str:
    """Masks Card: 4111222233334444 -> 4111 **** **** 4444"""
    clean = card_number.replace(" ", "").replace("-", "")
    if len(clean) < 12:
        return "****"
    return f"{clean[:4]} **** **** {clean[-4:]}"


def mask_account_number(acc_num: str) -> str:
    """Masks Account: 100012345678 -> *******5678"""
    if not acc_num or len(acc_num) < 4:
        return "****"
    return "*" * (len(acc_num) - 4) + acc_num[-4:]


def encrypt_data(plaintext: str, key: str = "FinXCoreDefaultEncryptionKey2026") -> str:
    """Simulated deterministic field-level reversible encryption."""
    if not plaintext:
        return ""
    key_bytes = hashlib.sha256(key.encode()).digest()
    text_bytes = plaintext.encode("utf-8")
    xor_bytes = bytes([b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(text_bytes)])
    return "ENC:" + base64.urlsafe_b64encode(xor_bytes).decode("utf-8")


def decrypt_data(ciphertext: str, key: str = "FinXCoreDefaultEncryptionKey2026") -> str:
    """Decrypts ciphertext created with encrypt_data."""
    if not ciphertext or not ciphertext.startswith("ENC:"):
        return ciphertext
    try:
        raw_b64 = ciphertext[4:]
        xor_bytes = base64.urlsafe_b64decode(raw_b64.encode("utf-8"))
        key_bytes = hashlib.sha256(key.encode()).digest()
        plain_bytes = bytes([b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(xor_bytes)])
        return plain_bytes.decode("utf-8")
    except Exception:
        return "[ENCRYPTED]"
