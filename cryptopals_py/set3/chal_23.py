from mersenne_twister import MersenneTwister
import time

f = 1812433253
m = 397
u = 11
s = 7
b = 0x9D2C5680
t = 15
c = 0xEFC60000
l = 18

def round1(y):
    if y > 2**32-1:
        raise ValueError("Not 32 bit")
    return y ^ (y>>18)

def round1_un(y):
    f1 = y & 0xFFFFC000
    f2 = ((y&0xFFFC0000)>>18) ^ y

    return f1 | f2


def round2(y):
    if y > 2**32-1:
        raise ValueError("Not 32 bit")
    return y^((y<<t)&c)

def round2_un(y):
    f1 = y & 0x0001ffff
    f2 = (y&0xFFFE0000) ^ (((y<<15)&0xFFFE0000) & c)

    return f1 | f2

def round3(y):
    if y > 2**32-1:
        raise ValueError("Not 32 bit")
    return y^((y<<s)&b)

def check_bit(i, b):
    # print("Checking {}".format(i))
    i = 32-i-1
    if i >= 32:
        raise ValueError("Failed Round3")
    return (b>>i) & 1

def ith(i, y):
    i = 32-i-1
    return (y>>i) & 1

def get_ith(i, y, b, off):
    if not check_bit(i, b):
        # print("ith for {} is not set, returning {} for y {}".format(i, ith(i, y), y))
        return ith(i, y)
    return ith(i, y) ^ get_ith(i+off, y, b, off)

def round3_un(y):
    f1 = y & 0x0000007F
    f2 = 0
    for i in range(25):
        # print("checking {}".format(i))
        f2 = f2 | get_ith(i, y, b, 7)
        f2 = f2 << 1
        # print("got {}".format(i))

    f2 = f2 << 6
    return f1 | f2

def round4(y):
    if y > 2**32-1:
        raise ValueError("Not 32 bit")
    return y^(y>>u)

def round4_un(y):
    f1 = y & 0xFFE00000
    f2 = 0
    f3 = 0
    for i in range(11):
        f2 = f2 << 1
        f2 = f2 | ith(i, y) ^ ith(i+11, y)
    f2 = f1 | (f2 << 10)

    for i in range(11, 21):
        f3 = f3 << 1
        f3 = f3 | ith(i, f2) ^ ith(i+11, y)

    return f2 | f3


def untemper(y):
    y = round1_un(y)
    y = round2_un(y)
    y = round3_un(y)
    y = round4_un(y)
    return y

if __name__ == '__main__':
    state = []
    m = MersenneTwister(int(time.time()))

    for i in range(624):
        state.append(untemper(m.get_random_number()))

    guess_m = MersenneTwister()
    guess_m.state = state.copy()
    guess_m.index = 624

    for i in range(624):
        assert guess_m.get_random_number() == m.get_random_number()

    print('[+] DONE!')
