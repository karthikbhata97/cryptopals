#! /usr/bin/python3
from Crypto.Cipher import AES


def AES_ECB_encrypt(key, data):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(data)


def AES_ECB_decrypt(key, ct):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.decrypt(ct)


def pkcs7pad(data, block_size=16):

    pad_len = block_size - (len(data) % block_size)

    return data + chr(pad_len).encode('utf-8') * pad_len


def xor(pt, key):
    if len(key) < len(pt):
        key = (len(pt)//len(key)) * key + key
        key = key[:len(pt)]

    enc = [p^k  for p, k in zip(pt, key)]
    return bytes(enc)


def unpad(data):
    pad_len = data[-1]

    return data[:-pad_len]


def AES_CBC_encrypt(key, iv, data, block_size=16):
    data_pad = pkcs7pad(data, block_size=block_size)

    res = b''

    for i in range(0, len(data_pad), block_size):
        block = data_pad[i:i+block_size]
        xor_block = xor(block, iv)
        enc_block = AES_ECB_encrypt(key, xor_block)

        res += enc_block
        iv = enc_block

    return res


def AES_CBC_decrypt(key, iv, ciphertext, block_size=16):
    assert(len(ciphertext)%block_size == 0)

    data = b''

    for i in range(0, len(ciphertext), block_size):
        block = ciphertext[i:i+block_size]

        dec_block = AES_ECB_decrypt(key, block)

        data += xor(dec_block, iv)

        iv = block

    data = pkcs7_validate(data)
    return data


def pkcs7_validate(data, blocksize=16):
    plen = data[-1]
    if plen > blocksize or not plen:
        raise ValueError('InvalidPadding')

    for i in data[-plen:]:
        if i != plen:
            raise ValueError('InvalidPadding')

    return data[:-plen]

