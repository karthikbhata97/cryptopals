from common import AES_ECB_encrypt, pkcs7pad, unpad, AES_ECB_decrypt
from os import urandom

KEY = urandom(16)

def parser(encoded_data):

    key_val = encoded_data.split('&')

    profile_d = dict()

    for kv in key_val:
        key, val = kv.split('=')

        profile_d[key] = val

    return profile_d


def encode_profile(profile_d):
    enc = 'email=%s&uid=%d&role=%s' % (profile_d['email'], profile_d['uid'], profile_d['role'])

    return enc


def profile_for(email):

    profile_d = {'uid': 10, 'role': 'user'}
    profile_d['email'] = email

    return profile_d


def encrypt_profile(encoded_profile):
    global KEY

    data = pkcs7pad(encoded_profile)

    return AES_ECB_encrypt(KEY, data)


def decrypt_profile(enc_profile):
    global KEY

    profile = AES_ECB_decrypt(KEY, enc_profile)
    return unpad(profile)


if __name__ == '__main__':

    print('[*] Testing...')
    p = profile_for('foo@bar.com')
    e = encode_profile(p)
    enc = encrypt_profile(e.encode('utf-8'))
    dec = decrypt_profile(enc).decode('utf-8')
    parsed = parser(e)
    print(p)
    print(e)
    print(parsed)

    print('[#] Attacking')
    p = profile_for('foooo@bar.com')
    e = encode_profile(p)
    enc = encrypt_profile(e.encode('utf-8'))[:-16]

    newp = profile_for('fo@bar.com' + pkcs7pad('admin'.encode('utf-8')).decode('utf-8'))
    e = encode_profile(newp)
    newenc = encrypt_profile(e.encode('utf-8'))[16:32]

    dec = decrypt_profile(enc+newenc).decode('utf-8')
    parsed = parser(dec)

    print(dec)
    print(parsed)

