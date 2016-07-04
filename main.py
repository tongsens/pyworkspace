#!/usr/bin/python
# coding=utf-8

from readelf import *
from simhash import *
import sqlite3
import sys

def createTab():
    cx = sqlite3.connect('c:\elfcollect\simhash.db')
    cu = cx.cursor()
    cu.execute('CREATE TABLE simhash (id INTEGER PRIMARY KEY, malname varchar(10), rodata varchar(100), strtab varchar(100))')

def elfSearch(filename):
    cx = sqlite3.connect('c:\elfcollect\simhash.db')
    cu = cx.cursor()
    elf = ReadElf(filename)
    hash_rodata = simhash(elf.getRodata())
    hash_strtab = simhash(elf.getStrtab())
    cu.execute('SELECT * FROM simhash')
    res = cu.fetchall()

    flag = 0
    for line in res:
        rodata_han = hash_rodata.hamming_distance(int(line[2]))
        rodata_rate = hash_rodata.similarity(int(line[2]))
        strtab_han = hash_strtab.hamming_distance(int(line[3]))
        strtab_rate = hash_strtab.similarity(int(line[3]))
        print "hamdistance:",rodata_han,'   ','similarity rate:',rodata_rate
        if rodata_han<20 and rodata_rate>0.9:
            print "This elf file is very similarity than ",line[1]
            print "hamdistance:",rodata_han,'   ','similarity rate:',rodata_rate
            flag = 1
            break

    if flag==0:
        malname = filename.split('\\')[-1]
        try:
            sql_cmd = "INSERT INTO simhash (malname,rodata,strtab) VALUES ('%s', '%s','%s')"%(malname, str(hash_rodata.getHash()), str(hash_strtab.getHash()))
            cu.execute(sql_cmd)
            cx.commit()
            print "insert file simhash to database"
            win_cmd = 'xcopy '+filename+' c:\\elfcollect\\file'
            os.system(win_cmd)
            print "copy file to c:\\elfcollect\\file"
        except:
            print "insert fail"

if __name__ == '__main__':
    #createTab()
    #filepath =  r'C:\Users\Administrator\Desktop\linuxmal\1mal'
    filepath = sys.argv[1]
    elfSearch(filepath)
