#!/usr/bin/env python

import struct
import sys

orig = sys.argv[1]
i = int(orig, 0)
new = hex(struct.unpack("<I", struct.pack(">I", i))[0])
print '\\x' + '\\x'.join([new[i:i+2] for i in range(2, len(new), 2)])
