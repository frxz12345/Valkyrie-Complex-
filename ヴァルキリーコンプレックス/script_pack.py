import os
import struct

game = 'VC'
file = 'Script.pak'
xor = 0x58
xor2 = 0x24


def 解包(p1, file):
    f = open(file, 'rb')
    fl = f.read()
    info = fl[24:28]
    cont = 0
    for i in range(len(info) - 1, -1, -1):
        t = info[i]
        t = t ^ xor
        if i != 0:
            cont = cont + t * 16 ** (2 * i)
        else:
            cont = cont + t
    print('文件数：', cont)
    # exit(1)
    info = fl[28:32]
    cont1 = 0
    for j in range(len(info) - 1, -1, -1):
        t = info[j]
        t = t ^ xor
        if j != 0:
            cont1 = cont1 + t * 16 ** (2 * j)
        else:
            cont1 = cont1 + t
    textdatastart = cont1
    filenamepos = 32 + cont * 16
    for i in range(cont):
        x = 32 + i * 16
        y = 32 + i * 16 + 16
        info = fl[x + 4:x + 8]
        cont1 = 0
        for j in range(len(info) - 1, -1, -1):
            t = info[j]
            t = t ^ xor
            if j != 0:
                cont1 = cont1 + t * 16 ** (2 * j)
            else:
                cont1 = cont1 + t
        filenamelen = cont1
        # print(textdatastart)
        info = fl[x + 12:x + 16]
        cont1 = 0
        for j in range(len(info) - 1, -1, -1):
            t = info[j]
            t = t ^ xor
            if j != 0:
                cont1 = cont1 + t * 16 ** (2 * j)
            else:
                cont1 = cont1 + t
        filesize = cont1
        # print(filesize)
        # exit(1)
        info = fl[x + 8:x + 12]
        cont1 = 0
        for j in range(len(info) - 1, -1, -1):
            t = info[j]
            t = t ^ xor
            if j != 0:
                cont1 = cont1 + t * 16 ** (2 * j)
            else:
                cont1 = cont1 + t
        filepos = cont1
        # print(hex(filepos))
        # exit(1)
        filename = ''
        fl1 = len(fl[filenamepos + 0:filenamepos + filenamelen]) * [b'']
        fl[filenamepos + 0:filenamepos + filenamelen].decode('cp932')
        for i in range(len(fl1)):
            t = fl[filenamepos + i]
            t = t ^ xor
            t = hex(t).replace('0x', '')
            if len(t) % 2 != 0:
                t = '0' + t
            fl1[i] = bytes.fromhex(t)
            filename = filename + fl1[i].decode('cp932')
        filename = filename.replace('\x00', '')
        filenamepos = filenamepos + len(fl1) + 1
        f1 = open(p1 + filename, 'wb')
        dec = fl[filepos:filepos + filesize]
        for i in dec:
            t = (i ^ xor2) - 1
            if t < 0x0:
                t = i
                bt = struct.pack('B', t)
                f1.write(bt)
            else:
                bt = struct.pack('B', t)
                f1.write(bt)
            # if t < 0:
            #     bt = struct.pack('B', i)
            #     f1.write(bt)
            # else:
            #     bt = struct.pack('B', t)
            #     f1.write(bt)
        # f1.write(fl[filesize:filesize + filepos])
        print(filename)
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
fw = open('' + file.replace('.pak', '.pak'), 'wb')
l1 = len(files) * [0]
i = 0
fw.write(b'\x82\x75\x82\x62\x90\xBB\x95\x69\x94\xC5')  ##文件头
fw.write(b'\x00' * 14)
z = len(os.listdir(p2))  # 计算文件数
z = hex(z).replace('0x', '')
if len(z) % 2 != 0:
    z = '0' + z
z = bytes.fromhex(z)
zc = 4 - len(z)
z = b'\x00' * zc + z
for i in range(3, -1, -1):  # 写入计算文件数
    t = struct.pack('B', z[i] ^ xor)
    fw.write(t)

textdatastart = len(files) * 16 + 0
for i in files:
    textdatastart = textdatastart + len(i) + 1

z = hex(textdatastart).replace('0x', '')
if len(z) % 2 != 0:
    z = '0' + z
z = bytes.fromhex(z)
zc = 4 - len(z)
z = b'\x00' * zc + z
for i in range(3, -1, -1):  # 写入文件总大小
    t = struct.pack('B', z[i] ^ xor)
    fw.write(t)
# exit(1)
'''
? -> ?
'''
fs = 0
for file in files:
    fs = fs + len(file) + 1
st = len(files) * 16 + 24 + 8 + fs
stats = 0
l1[0] = st
for file in files:
    if i == 0:
        l1[i] = st + stats
    else:
        l1[i] = l1[i - 1] + stats
    i = i + 1
    stats = os.stat(p2 + file).st_size
i = 0
xor1 = struct.pack('B', xor)
for file in files:
    bt = 16 * [xor1]
    # b0 = file
    # j = 0
    # for b in b0:
    #     t = b.encode('cp932')
    #     t = t.hex()
    #     t = int(t, 16)
    #     bt[j] = struct.pack('B', t ^ xor)
    #     j = j + 1
    filenamelen = len(file)

    z = hex(filenamelen).replace('0x', '')
    if len(z) % 2 != 0:
        z = '0' + z
    z = bytes.fromhex(z)
    zc = 4 - len(z)
    z = b'\x00' * zc + z
    j = len(z) - 1
    for i1 in range(4, 8):  # 文件名长度
        t = struct.pack('B', z[j] ^ xor)
        bt[i1] = t
        j = j - 1
    z = hex(l1[i]).replace('0x', '')
    if len(z) % 2 != 0:
        z = '0' + z
    z = bytes.fromhex(z)
    zc = 4 - len(z)
    z = b'\x00' * zc + z
    j = len(z) - 1
    for i1 in range(8, 12):  # 位置
        t = struct.pack('B', z[j] ^ xor)
        bt[i1] = t
        j = j - 1
    stats = os.stat(p2 + file).st_size
    z = hex(stats).replace('0x', '')
    if len(z) % 2 != 0:
        z = '0' + z
    z = bytes.fromhex(z)
    zc = 4 - len(z)
    z = b'\x00' * zc + z
    j = len(z) - 1
    for i1 in range(12, 16):  # 大小
        t = struct.pack('B', z[j] ^ xor)
        bt[i1] = t
        j = j - 1
    for k in bt:
        fw.write(k)
    i = i + 1
for file in files:
    file = file.encode('cp932')
    for j in file:
        j = struct.pack('B', j ^ xor)
        fw.write(j)
    fw.write(xor1)
for file in files:
    # print(file)
    f = open(p2 + file, 'rb')
    stats = os.stat(p2 + file).st_size
    b = f.read()
    if xor != 0:
        for i in b:
            j = (i + 1) ^ xor2
            if j > 0xff:
                j = i
            bt = struct.pack('B', j)
            fw.write(bt)
    else:
        fw.write(b)
    f.close()
fw.close()
files = os.listdir(p1)
# for i in files:
#     os.remove(p1 + i)
f = open('script.pak', 'rb')
b = f.read()
f.close()
p2 = './Pack\\'
if not os.path.exists(p1):
    os.mkdir(p2)
f = open('./Pack\script.pak', 'wb')
f.write(b)
f.close()
