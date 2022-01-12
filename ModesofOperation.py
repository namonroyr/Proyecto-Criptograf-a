def xor_bytes(a, b):
    """ Returns a new byte array with the elements xor'ed. """
    return bytes(i^j for i, j in zip(a, b))

def split_blocks(message, block_size=16, require_padding=True):
    assert len(message) % block_size == 0 or not require_padding
    return [message[i:i+16] for i in range(0, len(message), block_size)]

def encrypt_cbc(self, criptosys, plaintext, iv, cripto):
    """
    Encrypts `plaintext` using CBC mode and PKCS#7 padding, with the given
    initialization vector (iv).
    """
    assert len(iv) == 16

    blocks = []
    previous = iv
    for plaintext_block in split_blocks(plaintext):
        # CBC mode encrypt: encrypt(plaintext_block XOR previous)
        block = criptosys.encrypt(xor_bytes(plaintext_block, previous))
        blocks.append(block)
        previous = block

    return b''.join(blocks)

def decrypt_cbc(self , criptosys, ciphertext, iv):
    """
    Decrypts `ciphertext` using CBC mode and PKCS#7 padding, with the given
    initialization vector (iv).
    """
    assert len(iv) == 16

    blocks = []
    previous = iv
    for ciphertext_block in split_blocks(ciphertext):
        # CBC mode decrypt: previous XOR decrypt(ciphertext)
        blocks.append(xor_bytes(previous, criptosys.decrypt(ciphertext_block)))
        previous = ciphertext_block

    return b''.join(blocks)
