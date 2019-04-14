#!/usr/bin/env python

import numpy
import struct
import sys
import bisect

SIZE64 = 64
CUT64 = 0.95
CUT = 40

def getHash64(hsh, oid):
    return hsh[oid * SIZE64 : (oid + 1) * SIZE64]

def getDif(x, y, i):
    if x[i] > y[i]: return getDif(y, x, i)
    d = bisect.bisect_left(all_stats[i], y[i]) - bisect.bisect_right(
        all_stats[i], x[i])
    if d < 0: d = 0
    return d

def getDifx(x, y):
    delta = 0
    for i in xrange(SIZE64):
        delta += getDif(x, y, i)
    return delta * 1.0 / SIZE64

src = sys.argv[1]
tgt = src
if len(sys.argv) > 2:
    tgt = sys.argv[2]
if len(sys.argv) > 3:
    CUT = int(sys.argv[3])
    
print src
print tgt

raw = open(src + '/hsh64', 'rb').read()
fmt = '%df' %(len(raw)/4)
hsh_s = struct.unpack(fmt, raw)
mrt_s = open(src + '/mrt').read()

if tgt == src:
    hsh_t = hsh_s
    mrt_t = mrt_s
else:
    raw = open(tgt + '/hsh64', 'rb').read()
    fmt = '%df' %(len(raw)/4)
    hsh_t = struct.unpack(fmt, raw)
    mrt_t = open(tgt + '/mrt').read()
    
maxid_s = len(hsh_s) / SIZE64
maxid_t = len(hsh_t) / SIZE64
CUT = maxid_t / CUT

all_stats = []
for i in xrange(SIZE64):
    all_stats.append([])
    
for x in xrange(maxid_t):
    if mrt_t[x] == '0': continue
    for i in xrange(SIZE64):
        all_stats[i].append(hsh_t[x*SIZE64 + i])
for i in xrange(SIZE64):
    all_stats[i] = sorted(all_stats[i])
    
for x in xrange(maxid_s):
    if mrt_s[x] == '0': continue
    out = []
    miny = 0
    if src == tgt: miny = x + 1
    for y in xrange(miny, maxid_t):
        if mrt_t[y] == '0': continue
        hx = getHash64(hsh_s, x)
        hy = getHash64(hsh_t, y)
        if numpy.inner(hx, hy) > CUT64:
            score = getDifx(hx, hy)
            if score < CUT:
                out.append((score, y))
    if out:
        l = str(x)
        for z in sorted(out):
            l += ' ' + str(int(z[0])) + ' ' + str(z[1])
        print l
