#!/usr/bin/env python

from des_wrapper import des_encrypt
from task2 import (strtobin, bintostr, binlist)
import sys


in_ = sys.argv[1].strip()
out_ = sys.argv[2].strip()
key = sys.argv[3].strip()

with open(in_, 'r') as f:
    plaintext = f.read()

key = strtobin(key.decode('hex'))
ciphertext = des_encrypt(key, strtobin(plaintext))

with open(out_, 'w') as f:
    f.write(bintostr(binlist(ciphertext)))
