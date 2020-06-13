#!python3

from numpy import cumsum, trapz

def gini(values):
    sorted_values = sorted([0.] + values)
    bases = cumsum(sorted_values)/sum(values)

    return 1. - 2.*trapz( bases, dx=(1./len(values)) )

def bottom_top(values, btm_ratio=0.1, top_ratio=0.1):
    size = len(values)
    btm_num = int(btm_ratio*size)
    top_num = int(top_ratio*size)
    sorted_values = sorted(values)
    return sum(sorted_values[:btm_num]), sum(sorted_values[size-top_num:])