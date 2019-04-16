from chal_10 import AES_CBC_encrypt
from common import AES_ECB_encrypt, pkcs7pad
from random import randint
from os import urandom


def random_encrypt(data):
    key = urandom(16)
    iv = urandom(16)

    mode = randint(0, 1)

    data = urandom(randint(10, 15)) + data + urandom(randint(10, 15))
    if mode == 0:
        data = pkcs7pad(data)
        return AES_ECB_encrypt(key, data), 1
    else:
        return AES_CBC_encrypt(key, iv, data), 0


def is_ecb(data, blocksize=16):
    assert(len(data)%blocksize==0)

    seen = []
    for i in range(0, len(data), blocksize):
        curr = data[i:i+blocksize]
        if curr in seen:
            return True
        seen.append(curr)

    return False


if __name__ == '__main__':
    for i in range(100):
        enc, mode = random_encrypt(b'A'*16*3)
        if is_ecb(enc) == mode:
            print('[+] Right guess: ', 'ECB' if mode else 'CBC')
        else:
            print('[-] Wrong guess: ', 'ECB' if not mode else 'CBC', '\nTruth: ', 'ECB' if mode else 'CBC')



