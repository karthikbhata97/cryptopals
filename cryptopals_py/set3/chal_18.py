from common import AES_ECB_encrypt, AES_ECB_decrypt, xor
from base64 import b64decode, b64encode
from struct import pack
import sys


def counter():
    c = 0
    while True:
        yield c
        c += 1

def AES_CTR_crypt(key, nonce, data, blocksize=16):
    nonce_b = pack("<Q", nonce)
    ctr = counter()

    res = b''
    for i in range(0, len(data), blocksize):
        c = pack("<Q", next(ctr))
        keystream = AES_ECB_encrypt(key, nonce_b + c)
        res += xor(data[i:i+blocksize], keystream)

    return res



if __name__ == '__main__':

    ct = "L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ=="
    ct = b64decode(ct)

    key = b"YELLOW SUBMARINE"
    nonce = 0
    test = b"This has to be !"
    # print(b64encode(AES_CTR_crypt(key, nonce, test)))
    dec = AES_CTR_crypt(key, nonce, ct)
    print(dec)
    print(len(dec))
    # assert(AES_CTR_crypt(key, nonce, dec) == ct)
