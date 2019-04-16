from chal_10 import AES_CBC_encrypt, AES_CBC_decrypt
from os import urandom

key = urandom(16)
iv = urandom(16)


def encode_encrypt(userdata):
    prefix = "comment1=cooking%20MCs;userdata="
    postfix = ";comment2=%20like%20a%20pound%20of%20bacon"

    data = prefix + userdata + postfix
    data = data.encode('utf-8')
    return AES_CBC_encrypt(key, iv, data)

def decrypt_decode(encrypted_data):
    data = AES_CBC_decrypt(key, iv, encrypted_data)
    data = data.decode('utf-8', errors='ignore').split(';')

    print(data)

    all_kv = [kv.split('=') for kv in data]
    print(all_kv)

    return ['admin', 'true'] in all_kv


def bitflip(sample):
    payload = bytearray()
    for c in sample:
        payload.append(c^0x1)

    return bytes(payload)


def attack(blocksize=16):
    userdata_prepad = ''

    baselen = len(encode_encrypt(userdata_prepad))

    while len(encode_encrypt(userdata_prepad)) == baselen:
        userdata_prepad += 'A'

    userdata_prepad = userdata_prepad[:-1] #+ blocksize * 'A'

    payload = bitflip(";admin=true".encode('utf-8')).decode('utf-8')

    ciphertext = encode_encrypt(userdata_prepad + payload)

    for i in range(0, len(ciphertext), blocksize):
        block = ciphertext[i:i+blocksize]

        cipher_mod = block
        cipher_mod = bitflip(block)

        try:
            if decrypt_decode(ciphertext[:i] + cipher_mod + ciphertext[i+blocksize:]):
                return '[+] Successful'
        except:
            pass

    return '[-] Failed'


if __name__ == '__main__':
    print(attack())


