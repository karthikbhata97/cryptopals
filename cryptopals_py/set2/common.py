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
    assert(len(pt)==len(key))
    if len(key) < len(pt):
        key = (len(pt)//len(key)) * key + key
        key = key[:len(pt)]

    enc = ""

    enc = [p^k  for p, k in zip(pt, key)]
    return bytes(enc)


def unpad(data):
    pad_len = data[-1]

    return data[:-pad_len]


