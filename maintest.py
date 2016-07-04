__author__ = 'Administrator'

from readelf import *
from simhash import *

if __name__ == '__main__':
    filepath1 = r"C:\Users\Administrator\Desktop\linuxmal\tmp"
    filepath2 = r"C:\Users\Administrator\Desktop\linuxmal\sshd2"
    fpstr1 = ReadElf(filepath1)
    fpstr2 = ReadElf(filepath2)
    str1 = fpstr1.getRodata()
    str2 = fpstr2.getRodata()
    tmplist = []
    for line in str1:
        if line in str2:
            tmplist.append(line)
    print '#######################'
    for line in str1:
        if line not in tmplist:
            print line
    print '#######################'
    for line in str2:
        if line not in tmplist:
            print line