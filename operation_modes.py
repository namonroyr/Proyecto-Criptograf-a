import AES

def xor_bytes(a, b):
    """ Returns a new byte array with the elements xor'ed. """
    return bytes(i^j for i, j in zip(a, b))

def split_blocks(message, block_size=16, require_padding=True):
    assert len(message) % block_size == 0 or not require_padding
    return [message[i:i+16] for i in range(0, len(message), block_size)]

def pad(plaintext):
    """
    Pads the given plaintext with PKCS#7 padding to a multiple of 16 bytes.
    Note that if the plaintext size is a multiple of 16,
    a whole block will be added.
    """
    padding_len = 16 - (len(plaintext) % 16)
    padding = bytes([padding_len] * padding_len)
    return plaintext + padding

def unpad(plaintext):
    """
    Removes a PKCS#7 padding, returning the unpadded text and ensuring the
    padding was correct.
    """
    padding_len = plaintext[-1]
    assert padding_len > 0
    message, padding = plaintext[:-padding_len], plaintext[-padding_len:]
    assert all(p == padding_len for p in padding)
    return message

def inc_bytes(a):
    """ Returns a new byte array with the value increment by 1 """
    out = list(a)
    for i in reversed(range(len(out))):
        if out[i] == 0xFF:
            out[i] = 0
        else:
            out[i] += 1
            break
    return bytes(out)

def encrypt_ecb(cipher, plaintext, iv, key):
    """
    Encrypts `plaintext` using ECB mode, with the given
    initialization vector (iv).
    """
    assert len(iv) == 16
    plaintext_padded = pad(plaintext)
    paddedSize = len(plaintext_padded) - len(plaintext)
    blocks = []
    previous = iv
    for plaintext_block in split_blocks(plaintext_padded):
        block = cipher.encrypt(plaintext_block)
        blocks.append(block)
        previous = block

    return b''.join(blocks), paddedSize

def decrypt_ecb(cipher, ciphertext, iv):
    """
    Decrypts `ciphertext` using CBC mode and PKCS#7 padding, with the given
    initialization vector (iv).
    """
    assert len(iv) == 16
    blocks = []
    previous = iv
    for ciphertext_block in split_blocks(ciphertext):
        blocks.append(cipher.decrypt(ciphertext_block))
        previous = ciphertext_block
    return unpad(b''.join(blocks))

def encrypt_cbc(cipher, plaintext, iv, key):
    """
    Encrypts `plaintext` using CBC mode and PKCS#7 padding, with the given
    initialization vector (iv).
    """
    assert len(iv) == 16
    plaintext_padded = pad(plaintext)
    paddedSize = len(plaintext_padded) - len(plaintext)
    blocks = []
    previous = iv
    for plaintext_block in split_blocks(plaintext_padded):
        block = cipher.encrypt(xor_bytes(plaintext_block, previous))
        blocks.append(block)
        previous = block
    return b''.join(blocks), paddedSize

def decrypt_cbc(cipher, ciphertext, iv):
    """
    Decrypts `ciphertext` using CBC mode and PKCS#7 padding, with the given
    initialization vector (iv).
    """
    print("Flag6.1")
    assert len(iv) == 16
    blocks = []
    previous = iv
    print("Flag6.2")
    for ciphertext_block in split_blocks(ciphertext):
        blocks.append(xor_bytes(previous, cipher.decrypt(ciphertext_block)))
        previous = ciphertext_block
    print("Flag6.3")
    return unpad(b''.join(blocks))

def encrypt_ofb(cipher, plaintext, iv):
    """
    Encrypts `plaintext` using OFB mode initialization vector (iv).
    """
    assert len(iv) == 16

    blocks = []
    previous = iv
    for plaintext_block in split_blocks(plaintext, require_padding=False):
            # OFB mode encrypt: plaintext_block XOR encrypt(previous)
            block = cipher.encrypt(previous)
            ciphertext_block = xor_bytes(plaintext_block, block)
            blocks.append(ciphertext_block)
            previous = block

    return b''.join(blocks)

def decrypt_ofb(cipher, ciphertext, iv):
    """
    Decrypts `ciphertext` using OFB mode initialization vector (iv).
    """
    assert len(iv) == 16
    blocks = []
    previous = iv
    for ciphertext_block in split_blocks(ciphertext, require_padding=False):
        block = cipher.encrypt(previous)
        plaintext_block = xor_bytes(ciphertext_block, block)
        blocks.append(plaintext_block)
        previous = block

    return b''.join(blocks)

def encrypt_ctr(cipher, plaintext, iv):
    """
    Encrypts `plaintext` using CTR mode with the given nounce/IV.
    """
    assert len(iv) == 16
    blocks = []
    nonce = iv
    for plaintext_block in split_blocks(plaintext, require_padding=False):
        # CTR mode encrypt: plaintext_block XOR encrypt(nonce)
        block = xor_bytes(plaintext_block, cipher.encrypt(nonce))
        blocks.append(block)
        nonce = inc_bytes(nonce)

    return b''.join(blocks)

def decrypt_ctr(cipher, ciphertext, iv):
    """
    Decrypts `ciphertext` using CTR mode with the given nounce/IV.
    """
    assert len(iv) == 16
    blocks = []
    nonce = iv
    for ciphertext_block in split_blocks(ciphertext, require_padding=False):
        # CTR mode decrypt: ciphertext XOR encrypt(nonce)
        block = xor_bytes(ciphertext_block, cipher.encrypt(nonce))
        blocks.append(block)
        nonce = inc_bytes(nonce)

    return b''.join(blocks)
