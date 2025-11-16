from itertools import cycle

import caesar


def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    result = []
    keyword = keyword.upper()
    start_key = ord("A")

    for letter, key in zip(plaintext, cycle(keyword)):
        shift = ord(key) - start_key
        encrypt_letter = caesar.encrypt_caesar(letter, shift)
        result.append(encrypt_letter)

    ciphertext = "".join(result)
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    result = []
    keyword = keyword.upper()
    start_key = ord("A")

    for letter, key in zip(ciphertext, cycle(keyword)):
        shift = ord(key) - start_key
        decrypt_letter = caesar.decrypt_caesar(letter, shift)
        result.append(decrypt_letter)

    plaintext = "".join(result)
    return plaintext
