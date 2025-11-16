def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    result = []
    alphabet_length = 26

    for letter in plaintext:
        if letter.isalpha():
            if letter.isupper():
                start_code = ord("A")
            else:
                start_code = ord("a")

            offset = (ord(letter) - start_code + shift) % alphabet_length
            result.append(chr(start_code + offset))
        else:
            result.append(letter)

    ciphertext = "".join(result)
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.
    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    result = []
    alphabet_length = 26

    for letter in ciphertext:
        if letter.isalpha():
            if letter.isupper():
                start_code = ord("A")
            else:
                start_code = ord("a")

            offset = (ord(letter) - start_code - shift) % alphabet_length
            result.append(chr(start_code + offset))
        else:
            result.append(letter)

    plaintext = "".join(result)
    return plaintext
