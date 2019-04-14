#!/usr/bin/env python
import struct, sys

class Dat:
    def __init__(self, dir):
        self.dir = dir + '/'
        self.mrt = list(open(self.dir + 'mrt', 'rb').read())
        leng = open(self.dir + 'len', 'rb').read()
        self.n = len(leng)/4
        self.len = struct.unpack('>%di' %self.n, leng)
        self.hsh = open(self.dir + 'hsh64', 'rb')
        if len(self.mrt) < self.n:
            self.mrt.extend([chr(0)] * (self.n - len(self.mrt)))
    
    def getSize(self):
        return self.n
        
    def getLen(self, i):
        return self.len[i]
    
    def getHash(self, i):
        self.hsh.seek(i * 256, 0)
        return self.hsh.read(256)
    
    def getMerit(self, i):
        return self.mrt[i]
    
    def setMerit(self, i, m):
        self.mrt[i] = m
        
    def saveMerit(self):
        open(self.dir + 'mrt', 'wb').write(''.join(self.mrt))
        
    def report(self):
        good = 0
        for m in self.mrt:
            if m != '0': good += 1
        print str(good), self.n
        print len(self.mrt)


totalMap = {}

def buildMap(src, doMatch = False):
    for i in xrange(src.getSize()):
        if src.getMerit(i) == '0': continue
        k = src.getLen(i)
        h = src.getHash(i)
        if k not in totalMap:
            totalMap[k] = []
        v = totalMap[k]
        doInsert = True
        if doMatch:
            for hh in v:
                if hh == h:
                    src.setMerit(i, '0')
                    print str(i) + ' is a duplicate!'
                    doInsert = False
                    break
        if doInsert:
            v.append(h)        
        
src = Dat(sys.argv[1])

if len(sys.argv) > 2:
    buildMap(Dat(sys.argv[2]))
    
buildMap(src, True)
src.saveMerit()
src.report()
