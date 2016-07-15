#!/usr/bin/python

import sys
import time
import os
import binascii
import cPickle as pickle
from des_wrapper import des_decrypt


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


def chunk(iterable, size):
    for pos in xrange(0, len(iterable), size):
        yield iterable[pos:pos + size]


def bintohex(l):
    s = "".join([str(e) for e in l])
    t = ''.join(chr(int(s[i:i + 8], 2)) for i in xrange(0, len(s), 8))
    return binascii.hexlify(t).upper()


def binlist(s):
    return [0 if c == '0' else 1 for c in s]


def binstr(l):
    return "".join([str(e) for e in l])


def enum_key(current):
    """Return the next key based on the current key as hex string.

    TODO: Implement the required functions.
    """
    bit_list = strtobin(current.decode('hex'))
    #print bit_list
    del bit_list[0::8]
    #print bit_list
    key_as_int = int(''.join([str(i) for i in bit_list]), 2)
    #print key_as_int
    key_as_int += 1
    next_bit_list = binlist(bin(key_as_int)[2:])
    #print next_bit_list
    next_bit_list = ([0] * (56 - len(next_bit_list))) + next_bit_list
    #print len(next_bit_list)
    parity_bit_list = []
    for part in chunk(next_bit_list, 7):
        parity_bit = 1 if part.count(1) % 2 == 0 else 0
        parity_bit_list += [parity_bit] + part

    next_ = bintohex(parity_bit_list)
    #print current, next_, parity_bit_list, next_bit_list, key_as_int, bin(key_as_int)
    #print parity_bit_list
    return next_


def save_progress(key, count, time, path='progress.pkl'):
    if os.path.isfile(path):
        with open(path, 'r') as file_:
            data = pickle.load(file_)
    else:
        data = {
            'key': None,
            'count': 0,
            'time': 0,
        }
    data['key'] = key
    data['count'] += count
    data['time'] += time
    print data
    with open(path, 'w') as file_:
        pickle.dump(data, file_)


def get_key(key, path='progress.pkl'):
    if os.path.isfile(path):
        with open(path, 'r') as file_:
            data = pickle.load(file_)
            return data.get('key')
    else:
        return key


def crack(ciphertext, plaintext, key, end_key=None):
    decrypted = ''
    plaintext = binstr(strtobin(plaintext))
    cipherbits = strtobin(ciphertext)
    count = 0
    start = time.time()
    key = get_key(key)
    try:
        while True:
            count += 1
            decrypted = des_decrypt(strtobin(key.decode('hex')), cipherbits)
            if key == end_key or decrypted == plaintext:
                save_progress(key, count, time.time() - start)
                break

            key = enum_key(key)
            if count % 10000 == 0:
                print plaintext
                print decrypted
                save_progress(key, count, time.time() - start)
                count = 0
                start = time.time()
    except KeyboardInterrupt:
        pass

    if key == end_key:
        print 'Did not find key'
    elif decrypted == plaintext:
        print 'Found key:', key


def main(argv):
    if argv[0] == 'enum_key':
        print (enum_key(argv[1]))
    elif argv[0] == 'crack':
        """TODO: Add your own code and do whatever you do.
        """
        ciphertext_file = argv[1]
        plaintext_file = argv[2]
        start_key = argv[3]
        end_key = argv[4]
        try:
            ciphertext = open(ciphertext_file, 'r').read()
            plaintext = open(plaintext_file, 'r').read()
        except:
            print ('File Not Found')
        crack(ciphertext, plaintext, start_key, end_key)
    else:
        raise Exception("Wrong mode!")

if __name__ == "__main__":
    main(sys.argv[1:])
