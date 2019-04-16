from chal_3 import EnglishCharFreq
from chal_2 import xor
import sys


if __name__ == '__main__':

    with open('4.txt', 'r') as f:
        cts = f.readlines()

    all_score = {}
    scorer = EnglishCharFreq()

    for item in cts:
        for i in range(256):

            hex_data = xor(item.strip(), hex(i)[2:])
            str_data = bytes.fromhex(hex_data).decode('utf-8')

            all_score[str_data] = scorer.score(str_data)


    sys.stdout.write(max(all_score, key=all_score.get))
