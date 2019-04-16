import base64
from Crypto.Cipher import AES


def hex2base64(hexdata):

    byte_data = bytes.fromhex(hexdata)

    b64_data = base64.b64encode(byte_data).decode('utf-8')

    return b64_data

def xor(pt, key):

    if len(key) < len(pt):
        key = (len(pt)//len(key)) * key + key
        key = key[:len(pt)]

    pt_b = bytes.fromhex(pt)
    key_b = bytes.fromhex(key)

    enc = ""

    for x, y in zip(pt_b, key_b):
        enc += chr(x ^ y)

    return enc.encode('utf-8').hex()


class EnglishCharFreq:

    def __init__(self):
        self.freq_order = "etaoin shrdlcumwfgypbvkjxqz$"
        freq_list = [(x[1], x[0]) for x in enumerate(self.freq_order[::-1])]
        self.freq = dict(freq_list)

    def score(self, data):
        res = 0
        data = data.lower()
        for char in data:
            res += self.freq.get(char, 0)

        return res


def break_single_key_xor(enc):

    ct = enc.hex()

    scorer = EnglishCharFreq()

    all_score = {}

    for i in range(256):
        hex_data = xor(ct, hex(i)[2:])

        data = bytes.fromhex(hex_data).decode('utf-8')

        all_score[i] = scorer.score(data)

    key = max(all_score, key=all_score.get)
    data = xor(ct, hex(key)[2:])
    data = bytes.fromhex(data).decode('utf-8')

    return data, key

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


def AES_ECB_encrypt(key, data):
    pt = pad(data)
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(pt)


def AES_ECB_decrypt(key, ct):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.decrypt(ct)


def is_ecb(data, size=16):

    if len(data) % size:
        return False

    data_l = [data[i:i+size] for i in range(0, len(data), size)]

    for item in data_l:
        if data_l.count(item) > 1:
            return True

    return False