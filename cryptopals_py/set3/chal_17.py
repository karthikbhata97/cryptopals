from common import AES_CBC_encrypt, AES_CBC_decrypt, pkcs7_validate, xor
from os import urandom
from random import randint
from base64 import b64decode


KEY = urandom(16)
IV = urandom(16)
current_pt = ""

def get_random_enc():
    global current_pt, KEY, IV

    with open('17.txt', 'r') as f:
        data = f.read().split('\n')

    current_pt = b64decode(data[randint(0, len(data)-1)])

    return AES_CBC_encrypt(KEY, IV, current_pt)


def padding_oracle(iv, ct):
    global KEY
    return AES_CBC_decrypt(KEY, iv, ct)


def crack_block(prev, ct, pad=0):
    blocksize = len(ct)

    known = bytearray([pad]*pad)

    for i in range(pad+1, blocksize+1):
        pad = xor(xor(bytes(known), bytes([i])), prev[blocksize-i+1:])

        for j in range(1, 256):
            prepad = prev[:blocksize-i] + bytes([j^i^prev[-i]]) + pad

            try:
                padding_oracle(prepad, ct)
                known.insert(0, j)
                break
            except ValueError as e:
                #print(e)
                pass

        assert(len(known)==i)
    return known


def guess_pad(iv, ct):
    blocksize = len(ct)

    for i in range(1, blocksize+1):
        new_iv = xor(iv, bytes(blocksize-i) + b'\xff' + bytes(i-1))

        try:
            padding_oracle(new_iv, ct)
            return i-1
        except ValueError:
            pass

    return blocksize


def crack_CBC_padding_oracle(ciphertext, blocksize=16):

    global IV
    known = bytearray()

    iv = IV
    p = 0
    for i in range(0, len(ciphertext), blocksize):
        if i+blocksize == len(ciphertext):
            p = guess_pad(iv, ciphertext[i:i+blocksize])

        known += crack_block(iv, ciphertext[i:i+blocksize], p)
        iv = ciphertext[i:i+blocksize]
        print('Cracked block %d: %s' % (i//blocksize, bytes(known).decode('utf-8')))

    return pkcs7_validate(bytes(known))


if __name__ == '__main__':

    ct = get_random_enc()

    assert(current_pt == crack_CBC_padding_oracle(ct))

