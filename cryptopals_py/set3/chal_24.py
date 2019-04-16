import sys
from mersenne_twister import MersenneTwister
from os import urandom
from random import randint
import time

def generate_stream(seed):
    if seed >= 2**16:
        raise ValueError("Please give a 16 bit seed")

    prng = MersenneTwister(seed)

    while True:
        rn = prng.get_random_number()
        yield rn & 0xFF
        yield (rn >> 8) & 0xFF
        yield (rn >> 16) & 0xFF
        yield (rn >> 24) & 0xFF


def encrypt(pt, key):

    ct = bytearray()
    stream = generate_stream(key)

    for l in pt:
        ct.append(l^next(stream))

    return bytes(ct)


decrypt = encrypt

def reset_token(seed):
    token = bytearray()
    prng = MersenneTwister(seed)

    for i in range(4):
        rn = prng.get_random_number()
        token.append(rn & 0xFF)
        token.append((rn >> 8) & 0xFF)
        token.append((rn >> 16) & 0xFF)
        token.append((rn >> 24) & 0xFF)

    return token


def is_valid_token(token):
    t = int(time.time())

    for i in range(t, t-24*60*60, -1):
        if reset_token(i) == token:
            return True

    return False


if __name__ == '__main__':
    random_data = urandom(randint(0, 100))
    known_data = b'A' * 15

    seed = randint(0, 2**16)
    encrypted = encrypt(random_data + known_data, seed)

    t = time.monotonic()

    for i in range(2**16):
        if not i % 1000:
            sys.stdout.write('.')
        if(decrypt(encrypted, i)[-15:] == known_data):
            assert i == seed
            print("\nSeed is {}".format(seed))

            break

    t = time.monotonic() - t

    print("Total time: {} seconds".format(t))

    token = reset_token(int(time.time()))
    assert is_valid_token(token)


