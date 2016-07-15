#!/usr/bin/env python

from des_wrapper import des_decrypt
from task2 import (strtobin, bintostr, binlist)
import sys


in_ = sys.argv[1].strip()
key = sys.argv[2].strip()

with open(in_, 'r') as f:
    ciphertext = f.read()

key = strtobin(key.decode('hex'))
print bintostr(binlist(des_decrypt(key, strtobin(ciphertext))))
