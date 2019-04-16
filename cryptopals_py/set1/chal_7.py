#! /usr/bin/python3.6

from Crypto.Cipher import AES
import base64

BLOCK_SZ = 16
pad = lambda x: (BLOCK_SZ-len(x)%BLOCK_SZ) * chr(0)

def AES_ECB_encrypt(key, data):
    pt = pad(data)
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(pt)


def AES_ECB_decrypt(key, ct):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.decrypt(ct)


if __name__ == '__main__':
    with open('7.txt') as f:
        ct = base64.b64decode(f.read())

    key = "YELLOW SUBMARINE"
    print(AES_ECB_decrypt(key, ct).decode('utf-8'))

