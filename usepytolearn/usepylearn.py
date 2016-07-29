__author__ = 'Administrator'

from getdata.getdata import *
from collections import defaultdict

def get_counts2(seq):
    counts = defaultdict(int)
    for x in seq:
        counts[x] += 1
    return counts

def counter(seq):
    from collections import Counter
    counts = Counter(seq)
    counts.most_common(10)

if __name__ == '__main__':
    gd = GetData()
    api_list, clss_list ,md_list = gd.getapidata(20)
    print counter(api_list[0])