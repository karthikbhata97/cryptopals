from common import AES_ECB_encrypt
import base64
from os import urandom
from common import pkcs7pad

KEY = urandom(16)

def encryption_oracle(mystring, unknown):
    global KEY
    data = pkcs7pad(mystring+unknown)
    return AES_ECB_encrypt(KEY, data)

def crack_byte_by_byte(data, blocksize=16):
    known = bytearray()

    while len(known) < len(data):
        block = len(known)//blocksize
        prepad = b'A' * (blocksize-(len(known)%blocksize)-1)

        offset = (blocksize*block, blocksize*(block+1))
        enc_actual = encryption_oracle(prepad, data)[offset[0]:offset[1]]

        for i in range(256):
            tmp = bytes(known) + bytes(bytearray([i]))

            tmp_enc = encryption_oracle(prepad, tmp)[offset[0]:offset[1]]

            if tmp_enc == enc_actual:
                known.append(i)
                print('Found %s' % (chr(i),))
                break

    return bytes(known)

if __name__ == '__main__':
    data_encoded = 'Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg\
                    aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq\
                    dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg\
                    YnkK'

    data = base64.b64decode(data_encoded)

    print(crack_byte_by_byte(data).decode('utf-8'))
