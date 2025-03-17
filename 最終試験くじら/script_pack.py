import os
import struct

file = 'Script.pak'
xor = 0XAA


def 解包(p1, file):
    f = open(file, 'rb')
    fl = f.read()
    info = fl[16:20]
    cont = 0
    for i in range(len(info) - 1, -1, -1):
        t = info[i]
        t = t ^ xor
        if i != 0:
            cont = cont + t * 16 ** (2 * i)
        else:
            cont = cont + t
    print('文件数：', cont)
    for i in range(cont):
        x = 24 + i * 40
        y = 24 + i * 40 + 40
        info = fl[x + 32:y - 4]
        cont1 = 0
        fl1 = len(fl[x:y - 8]) * [b'']
        filename = ''
        for i in range(len(fl1)):
            t = fl[x + i]
            t = t ^ xor
            t = hex(t).replace('0x', '')
            if len(t) % 2 != 0:
                t = '0' + t
            fl1[i] = bytes.fromhex(t)
            filename = filename + fl1[i].decode('cp932')
        filename = filename.replace('\x00', '')
        for j in range(len(info) - 1, -1, -1):
            t = info[j]
            t = t ^ xor
            if j != 0:
                cont1 = cont1 + t * 16 ** (2 * j)
            else:
                cont1 = cont1 + t
        filesize = cont1
        info = fl[x + 36:y]
        cont1 = 0
        for j in range(len(info) - 1, -1, -1):
            t = info[j]
            t = t ^ xor
            if j != 0:
                cont1 = cont1 + t * 16 ** (2 * j)
            else:
                cont1 = cont1 + t
        filepos = cont1
        print(filename)
        # print(hex(filesize))
        # print(hex(filepos))
        # print()
        f1 = open(p1 + filename, 'wb')
        dec = fl[filesize:filesize + filepos]
        for i in dec:
            t = 0xfe - i
            if t < 0:
                bt = struct.pack('B', i)
                f1.write(bt)
            else:
                bt = struct.pack('B', t)
                f1.write(bt)
        # f1.write(fl[filesize:filesize + filepos])
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
l1 = len(files) * [0]
i = 0
fw.write(b'\x46\x69\x6C\x65\x20\x50\x61\x63\x6B\x20\x31\x2E\x30\x30\x00\xAA')  ##文件头每个封包都一样
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
z = len(os.listdir(p2)) * 40 + 24
for i in os.listdir(p2):  # 计算文件总大小
    z = z + os.stat(p2 + i).st_size
z = hex(z).replace('0x', '')
if len(z) % 2 != 0:
    z = '0' + z
z = bytes.fromhex(z)
zc = 4 - len(z)
z = b'\x00' * zc + z
for i in range(3, -1, -1):  # 写入文件总大小
    t = struct.pack('B', z[i] ^ xor)
    fw.write(t)
'''
2A F4 4F 00 -> ?
'''
st = len(files) * 40 + 24
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
for file in files:
    bt = 40 * [b'\xAA']
    b0 = file
    j = 0
    for b in b0:
        t = b.encode('cp932')
        t = t.hex()
        t = int(t, 16)
        bt[j] = struct.pack('B', t ^ xor)
        j = j + 1
    z = hex(l1[i]).replace('0x', '')
    if len(z) % 2 != 0:
        z = '0' + z
    z = bytes.fromhex(z)
    zc = 4 - len(z)
    z = b'\x00' * zc + z
    j = len(z) - 1
    for i1 in range(32, 36):  # 位置
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
    for i1 in range(36, 40):  # 大小
        t = struct.pack('B', z[j] ^ xor)
        bt[i1] = t
        j = j - 1
    for k in bt:
        fw.write(k)
    i = i + 1
    # exit()
for file in files:
    print(file)
    f = open(p2 + file, 'rb')
    stats = os.stat(p2 + file).st_size
    b = f.read()
    if xor != 0:
        for i in b:
            j = 0xfe - i
            if j > 0:
                bt = struct.pack('B', j)
                fw.write(bt)
            else:
                bt = struct.pack('B', i)
                fw.write(bt)
    else:
        fw.write(b)
    f.close()
fw.close()
files = os.listdir(p1)
# for i in files:
#     os.remove(p1 + i)
