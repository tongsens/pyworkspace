#!/usr/bin/python
# coding=utf-8

import os
import shutil

class ReadElf():
    def __init__(self, filepath):
        self.filepath = filepath
        self.rodata = []
        self.strtab = []
        self.readString()

    #从二进制文件中读取字符串
    def getString(self,filename):
        ret_list = []
        with open(filename,'rb') as fp:
            buf = fp.read()
        tmp_str = ''
        for mchr in buf:
            if ord(mchr) in range(32,127):
                tmp_str += mchr
            else:
                if len(tmp_str)>4:
                    ret_list.append(tmp_str)
                tmp_str = ''
        return  ret_list

    #解压elf文件，获取符号表和字符串表
    def readString(self):
        if os.path.exists('mytmp'):
            shutil.rmtree('mytmp')
        try:
            os.mkdir('mytmp')
            zipcmd = '7z e '+self.filepath+' -omytmp'
            print zipcmd
            os.system(zipcmd)
            filerodata = 'mytmp'+ '\\' + '.rodata'
            filestrtab = 'mytmp'+ '\\' + '.strtab'
            self.rodata = self.getString(filerodata)
            self.strtab = self.getString(filestrtab)
            shutil.rmtree('mytmp')
        except:
            pass

    #返回字符串表
    def getRodata(self):
        return self.rodata

    #返回符号表
    def getStrtab(self):
        return self.strtab
