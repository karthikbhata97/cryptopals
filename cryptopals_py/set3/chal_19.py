from break_xor import break_single_key_xor
from chal_18 import AES_CTR_crypt
from os import urandom
from random import randint
from base64 import b64decode


key = urandom(16)
nonce = randint(0, 1<<63)


if __name__ == '__main__':
    with open('19.txt', 'r') as f:
        data = f.read().splitlines()

    mlen = 0
    ct = []

    for item in data:
        enc = AES_CTR_crypt(key, nonce, b64decode(item))
        mlen = max(mlen, len(enc))
        ct.append(enc)

    pt = [''] * len(ct)

    for i in range(mlen):
        curr = bytearray()
        ptr = []

        for j in range(len(ct)):
            if len(ct[j]) <= i:
                continue
            curr.append(ct[j][i])
            ptr.append(j)

        res = break_single_key_xor(bytes(curr))[0].encode('utf-8')

        for j in range(len(ptr)):
            pt[ptr[j]] += chr(res[j])


    for c in pt:
        print(c)
