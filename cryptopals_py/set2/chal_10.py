#! /usr/bin/python3
from common import AES_ECB_decrypt,  AES_ECB_encrypt, xor, pkcs7pad, unpad
from base64 import b64decode


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

    data = unpad(data)
    return data


if __name__ == '__main__':
    with open('10.txt', 'r') as f:
        b64data = f.read()
    
    data = b64decode(b64data)

    key = 'YELLOW SUBMARINE'.encode('utf-8')
    iv = b'\x00' * 16

    actual_data = AES_CBC_decrypt(key, iv, data)
    print(actual_data.decode('utf-8'))

    enc = AES_CBC_encrypt(key, iv, actual_data)

    assert(data==enc)
