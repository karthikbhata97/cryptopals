#! /usr/bin/python3.6

from chal_7 import AES_ECB_decrypt


def is_ecb(data, size=16):

    if len(data) % size:
        return False

    data_l = [data[i:i+size] for i in range(0, len(data), size)]

    for item in data_l:
        if data_l.count(item) > 1:
            return True

    return False


if __name__ == '__main__':

    with open('8.txt', 'r') as f:
        data = f.readlines()

    for item in data:
        item_data = bytes.fromhex(item.strip())
        if is_ecb(item_data):
            print(item)

