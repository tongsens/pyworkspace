__author__ = 'Administrator'

import os


def readfile():
    file = r'C:\Users\Administrator\Desktop\111'
    path_list = []
    for rt,dirs,files in os.walk(file):
        for f in files:
            path = os.path.join(rt, f)
            path_list.append(path)
    return path_list

def findkey(keyword):
    for file in readfile():
        with open(file, 'r') as fp:
            buf = fp.read()
            if buf.find(keyword)!=-1:
                print file


if __name__ == '__main__':
    findkey('svchost')