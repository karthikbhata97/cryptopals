from chal_2 import xor

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


if __name__ == '__main__':

    ct = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"

    print(break_single_key_xor(bytes.fromhex(ct)))
