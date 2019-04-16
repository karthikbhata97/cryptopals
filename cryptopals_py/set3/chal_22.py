from mersenne_twister import MersenneTwister
import time


def guess_random(real_random):
    guess_seed = int(time.time())
    guess_random = MersenneTwister(guess_seed).get_random_number()

    while(real_random != guess_random):
        guess_seed = guess_seed - 1
        guess_random = MersenneTwister(guess_seed).get_random_number()

    return guess_seed


if __name__ == '__main__':
    print('[+] Generating random number')
    time.sleep(MersenneTwister(int(time.time())).get_random_number()%50)

    real_random_obj = MersenneTwister(int(time.time()))
    real_random = real_random_obj.get_random_number()

    time.sleep(MersenneTwister(int(time.time())).get_random_number()%50)

    guess = guess_random(real_random)
    print('[+] Found the seed')

    assert guess == real_random_obj.seed


