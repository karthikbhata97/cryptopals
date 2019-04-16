from chal_2 import xor


if __name__ == '__main__':

    pt = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
    ct = "0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a\
26226324272765272a282b2f20430a652e2c652a3124333a653e2b20\
27630c692b20283165286326302e27282f"
    key = "ICE"
    key_hex = key.encode('utf-8').hex()

    pt_hex = pt.encode('utf-8').hex()
    assert(xor(pt_hex, key_hex)==ct)
