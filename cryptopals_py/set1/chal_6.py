#/usr/bin/python3.6
from chal_3 import break_single_key_xor, EnglishCharFreq
import base64
from chal_2 import xor


def hamming_distance(a: bytes, b: bytes):

    assert(len(a) == len(b))

    dist = 0

    for x, y in zip(a, b):
        xord_val = x ^ y
        dist += bin(xord_val).count('1')

    return dist


def guess_keysize(enc):
    score = {}
    for i in range(2, 40, 1):
        curr_score = 0
        times = 0
        for j in range(0, len(enc)-2*i, i):

            curr_score += hamming_distance(enc[j:j+i], enc[j+i:j+2*i])
            times += 1

        score[i] = curr_score/(times*i)

    return min(score, key=score.get)


def break_repeating_key_xor(enc):

    keysize = guess_keysize(enc)

    single_key_xor = [b""] * keysize

    for i in range(0, len(enc)):
        single_key_xor[i%keysize] += enc[i:i+1]

    key = ""
    for block in single_key_xor:
        res = break_single_key_xor(block)
        key += chr(res[1])

    assert(len(key)==keysize)

    data = xor(enc.hex(), key.encode('utf-8').hex())
    data = bytes.fromhex(data).decode('utf-8')

    return data, key


if __name__ == '__main__':

    s1 = "this is a test".encode('utf-8')
    s2 = "wokka wokka!!!".encode('utf-8')

    assert(hamming_distance(s1, s2)==37)

    with open('6.txt', 'r') as f:
        enc_data = base64.b64decode(f.read())

    broke = break_repeating_key_xor(enc_data)
    print(broke[0])

