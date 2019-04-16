import base64

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


if __name__ == '__main__':
    pt = "1c0111001f010100061a024b53535009181c"
    key = "686974207468652062756c6c277320657965"
    ct = "746865206b696420646f6e277420706c6179"

    assert(xor(pt, key)==ct)

