#!/usr/bin/env python
import random

b = [2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018]
a = [1, 40, 24, 26, 29, 80, 100, 36]

BASE = 1990

YEARS = 28

f = open('random.dat', 'w')
for offset in range(YEARS):
    date = BASE + offset
    value = random.randint(-500, 500)

    f.write(f'{date} {int(value)}\n')
f.close()



