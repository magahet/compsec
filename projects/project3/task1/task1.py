#!/usr/bin/python
import binascii
import sys
import time
from des import des


def bintohex(s):
    t = ''.join(chr(int(s[i:i + 8], 2)) for i in xrange(0, len(s), 8))
    return binascii.hexlify(t).upper()


def test():
    key1 = b"\0\0\0\0\0\0\0\0"
    key2 = b"\0\0\0\0\0\0\0\2"
    message1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    message2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
    test_des(key1, message1)
    test_des(key1, message2)
    test_des(key2, message1)
    test_des(key2, message2)


def test_des(key, message):
    k = des(key)
    c = k.des_encrypt(message)
    print c
    print (bintohex("".join([str(e) for e in c])))


def pad(message, block_size=8):
    '''Pads messages.'''
    message += '\x80'
    while len(message) % block_size != 0:
        message += '\0'
    return message


def depad(message, block_size=8):
    '''Depads messages.'''
    return message.strip('\0').strip('\x80')


def xor(l1, l2):
    return map(lambda x, y: x ^ y, l1, l2)


def strtobin(data):
    """Turn the string data, into a list of bits (1, 0)'s"""
    data = [ord(c) for c in data]
    l = len(data) * 8
    result = [0] * l
    pos = 0
    for ch in data:
        i = 7
        while i >= 0:
            if ch & (1 << i) != 0:
                result[pos] = 1
            else:
                result[pos] = 0
            pos += 1
            i -= 1

    return result


def bintostr(data):
    """Turn the list of bits -> data, into a string"""
    result = []
    pos = 0
    c = 0
    while pos < len(data):
        c += data[pos] << (7 - (pos % 8))
        if (pos % 8) == 7:
            result.append(c)
            c = 0
        pos += 1
    return ''.join([chr(c) for c in result])


def cbc_encrypt(message, key, iv, block_size=8):
    """
    Args:
      message: string, bytes, cannot be unicode
      key: string, bytes, cannot be unicode
    Returns:
      ciphertext: string
    """
    #TODO: Add your code here.
    k = des(key.decode('hex'))
    message = pad(message)
    cipher_block = strtobin(iv.decode('hex'))
    cipher_text = []
    for pos in xrange(0, len(message), block_size):
        bit_list = strtobin(message[pos:pos + block_size])
        cipher_block = k.des_encrypt(xor(bit_list, cipher_block))
        cipher_text += cipher_block
    return bintostr(cipher_text)


def cbc_decrypt(message, key, iv, block_size=8):
    """
    Args:
      message: string, bytes, cannot be unicode
      key: string, bytes, cannot be unicode
    Returns:
      plaintext: string
    """
    # TODO: Add your code here.
    k = des(key.decode('hex'))
    previous_cipher_block = strtobin(iv.decode('hex'))
    plain_text_list = []
    for pos in xrange(0, len(message), block_size):
        cipher_block = strtobin(message[pos:pos + block_size])
        bit_list = k.des_decrypt(cipher_block)
        plain_text_list += xor(bit_list, previous_cipher_block)
        previous_cipher_block = cipher_block
    return depad(bintostr(plain_text_list))


def main(argv):
    if len(argv) != 5:
        print ('Wrong number of arguments!\npython task1.py $MODE $INFILE $KEYFILE $IVFILE $OUTFILE')
        sys.exit(1)
    mode = argv[0]
    infile = argv[1]
    keyfile = argv[2]
    ivfile = argv[3]
    outfile = argv[4]
    message = None
    key = None
    iv = None
    try:
        message = open(infile, 'r').read()
        key = open(keyfile, 'r').read()
        iv = open(ivfile, 'r').read()
    except:
        print ('File Not Found')
    start = time.time()
    if mode == "enc":
        output = cbc_encrypt(message, key, iv)
    elif mode == "dec":
        output = cbc_decrypt(message, key, iv)
    else:
        print ("Wrong mode!")
        sys.exit(1)
    end = time.time()
    print ("Consumed CPU time=%f" % (end - start))
    open(outfile, 'w').write(output)

if __name__ == "__main__":
    main(sys.argv[1:])
