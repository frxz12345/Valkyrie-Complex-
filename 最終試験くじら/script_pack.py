import os
import struct

file = 'Script.pak'
key = 0xAA


def from_bytes(a: bytes):
    return int.from_bytes(a, byteorder='little')


def 解包(p1, file):
    f = open(file, 'rb')
    fl = f.read()
    filehead = fl[0:16]
    allfileszie = fl[20:24]
    data = fl[16:20]
    d = b''
    for i in data:
        i = i ^ key
        d = d + struct.pack('B', i)
    filecont = from_bytes(d)
    print('文件数：', filecont)
    for i in range(filecont):
        x = 24 + i * 40
        y = 24 + i * 40 + 40
        data = fl[x + 0:y - 8]
        d = b''
        for i in data:
            i = i ^ key
            d = d + struct.pack('B', i)
        filename = d.decode('cp932').replace('\x00', '')
        data = fl[x + 32:y - 4]
        d = b''
        for i in data:
            i = i ^ key
            d = d + struct.pack('B', i)
        pos = from_bytes(d)
        data = fl[x + 36:y]
        d = b''
        for i in data:
            i = i ^ key
            d = d + struct.pack('B', i)
        size = from_bytes(d)
        f1 = open(p1 + filename, 'wb')
        dec = fl[pos:pos + size]
        for i in dec:
            t = 0xfe - i
            if t < 0:
                bt = struct.pack('B', i)
                f1.write(bt)
            else:
                bt = struct.pack('B', t)
                f1.write(bt)
        f1.close()
    f.close()


p1 = './temp\\'
p2 = './cn\\'
if not os.path.exists(p1):
    os.mkdir(p1)
if not os.path.exists(p2):
    os.mkdir(p2)
解包(p1, file)
# exit(1)
files = os.listdir(p2)
fw = open('' + file.replace('.pak', '.new'), 'wb')
fw.write(b'\x46\x69\x6C\x65\x20\x50\x61\x63\x6B\x20\x31\x2E\x30\x30\x00\xAA')  ##文件头每个封包都一样
filecont = len(files)
data = struct.pack('i', filecont)
d = b''
for i in data:
    i = i ^ key
    d = d + struct.pack('B', i)
fw.write(d)  # 写入文件数
allfilesize = 24
for file in files:
    allfilesize = allfilesize + 40 + os.stat(p2 + file).st_size
data = struct.pack('i', allfilesize)
d = b''
for i in data:
    i = i ^ key
    d = d + struct.pack('B', i)
fw.write(d)  # 写入文件总大小
filestart = 24 + filecont * 40
pos = filestart
for file in files:
    fl = (32 - len(file))
    filename = file.encode('cp932') + b'\x00' * fl
    size = os.stat(p2 + file).st_size
    data = filename
    d = b''
    for i in data:
        i = i ^ key
        d = d + struct.pack('B', i)
    fw.write(d)
    data = struct.pack('i',pos)
    d = b''
    for i in data:
        i = i ^ key
        d = d + struct.pack('B',i)
    fw.write(d)
    data = struct.pack('i',size)
    d = b''
    for i in data:
        i = i ^ key
        d = d + struct.pack('B', i)
    fw.write(d)
    pos = pos + size
# exit(1)
for file in files:
    f = open(p2 + file, 'rb')
    data = f.read()
    f.close()
    d = b''
    for i in data:
        i0 = i
        i = 0xfe - i
        if i > 0:
            d = d + struct.pack('B', i)
        else:
            d = d + i0
    fw.write(d)
fw.close()
