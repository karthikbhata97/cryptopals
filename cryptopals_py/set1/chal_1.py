import base64

def hex2base64(hexdata):

    byte_data = bytes.fromhex(hexdata)

    b64_data = base64.b64encode(byte_data).decode('utf-8')

    return b64_data


if __name__ == '__main__':

    inp = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
    op = "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"

    assert(hex2base64(inp)==op)
