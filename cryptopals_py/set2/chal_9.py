#! /usr/bin/python3.6

def pad(data, block_size=16):

    pad_len = block_size - (len(data) % block_size)

    return data + chr(pad_len).encode('utf-8') * pad_len


if __name__ == '__main__':

    inp = 'YELLOW SUBMARINE'
    op = 'YELLOW SUBMARINE\x04\x04\x04\x04'
    assert(pad(inp.encode('utf-8'), 20)==op.encode('utf-8'))
