import os
import struct

game = 'ヴァルキリーコンプレックス'
arc = 'Script.pak'
key1 = 0x58
key2 = 0x24


def from_bytes(a: bytes):
    return int.from_bytes(a, byteorder='little')


def 解包(p1, file):
    f = open(file, 'rb')
    fl = f.read()
    data = fl[24:28]
    d = b''
    for i in data:
        i = i ^ key1
        d = d + struct.pack('B', i)
    filescont = from_bytes(d)
    print('文件数：', filescont)
    data = fl[28:32]
    d = b''
    for i in data:
        i = i ^ key1
        d = d + struct.pack('B', i)
    xx = from_bytes(d)
    filenamepos = 32 + filescont * 16
    print('文件名开始位置', filenamepos)
    for i in range(filescont):
        x = 32 + i * 16
        y = 32 + i * 16 + 16
        data = fl[x + 4:x + 8]
        d = b''
        for i in data:
            i = i ^ key1
            d = d + struct.pack('B', i)
        filenamelen = from_bytes(d)
        data = fl[x + 12:x + 16]
        d = b''
        for i in data:
            i = i ^ key1
            d = d + struct.pack('B', i)
        filesize = from_bytes(d)
        data = fl[x + 8:x + 12]
        d = b''
        for i in data:
            i = i ^ key1
            d = d + struct.pack('B', i)
        filepos = from_bytes(d)
        fl1 = len(fl[filenamepos + 0:filenamepos + filenamelen]) * [b'']
        d = b''
        for i in range(len(fl1)):
            t = fl[filenamepos + i]
            t = t ^ key1
            d = d + struct.pack('B', t)
        filename = d.decode('cp932').replace('\x00', '')
        filenamepos = filenamepos + len(fl1) + 1
        f1 = open(p1 + filename, 'wb')
        dec = fl[filepos:filepos + filesize]
        for i in dec:
            t = (i ^ key2) - 1
            if t < 0x0:
                t = i
                bt = struct.pack('B', t)
                f1.write(bt)
            else:
                bt = struct.pack('B', t)
                f1.write(bt)
        print(filename)
        f1.close()
    f.close()


p1 = './temp\\'
p2 = './cn\\'
if not os.path.exists(p1):
    os.mkdir(p1)
if not os.path.exists(p2):
    os.mkdir(p2)
解包(p1, arc)
# exit(1)
files = os.listdir(p2)
fw = open('' + arc.replace('.pak', '.pak.new'), 'wb')
l1 = len(files) * [0]
i = 0
fw.write(b'\x82\x75\x82\x62\x90\xBB\x95\x69\x94\xC5')  ##文件头
fw.write(b'\x00' * 14)
z = len(os.listdir(p2))  # 计算文件数
data = struct.pack('i', z)
d = b''
for i in data:
    i = i ^ key1
    i = struct.pack('B', i)
    fw.write(i)
textdatastart = len(files) * 16 + 0
for i in files:
    textdatastart = textdatastart + len(i) + 1
z = textdatastart
data = struct.pack('i', z)
d = b''
for i in data:
    i = i ^ key1
    i = struct.pack('B', i)
    fw.write(i)
fs = 0  # 文件名占用的字节数
for file in files:
    fs = fs + len(file) + 1
st = len(files) * 16 + 24 + 8 + fs
pos = st
data = b''
for file in files:
    filenamelen = len(file)
    size = os.stat(p2 + file).st_size
    _04 = b'\x00'*4
    data = data + _04
    data = data + struct.pack('i',filenamelen)
    data = data + struct.pack('i',pos)
    data = data + struct.pack('i',size)
    pos = pos + size
d = b''
for i in data:
    i = i ^ key1
    d = d + struct.pack('B', i)
fw.write(d)
data = b''
for file in files:
    data = data + file.encode('CP932') + b'\x00'
d = b''
for i in data:
    i = i ^ key1
    d = d + struct.pack('B', i)
fw.write(d)
for file in files:
    f = open(p2 + file, 'rb')
    stats = os.stat(p2 + file).st_size
    b = f.read()
    if key1 != 0:
        for i in b:
            j = (i + 1) ^ key2
            if j > 0xff:
                j = i
            bt = struct.pack('B', j)
            fw.write(bt)
    else:
        fw.write(b)
    f.close()
fw.close()
