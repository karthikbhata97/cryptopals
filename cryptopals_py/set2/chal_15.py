

def pkcs7_validate(data, blocksize=16):
    plen = data[-1]
    if plen > blocksize:
        raise ValueError('InvalidPadding')

    for i in range(plen):
        if data[-i] != plen:
            raise ValueError('InvalidPadding')


if __name__ == '__main__':
    pkcs7_validate(b'A'* 50)
