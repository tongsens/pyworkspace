__author__ = 'Administrator'
import yara

path = r'C:\Users\Administrator\Desktop\yara'
rules = yara.compile(filepaths={
    'namespaces':path
})
print path
