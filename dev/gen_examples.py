#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  gen_examples.py Author "Nathan Wycoff <nathanbrwycoff@gmail.com>" Date 01.31.2018

# Generate some examples of 1D Demand Zones to test the Linear Program.
# Notation is defined in a separate document.
import matplotlib.pyplot as plt
from scipy.special import binom
import numpy as np

# Bring in my combinatorics functions
execfile('comb_funcs.py')

## A single demand zone, the same length as a supply zone. The optimal solution is obvious.
# Define some parameters
p = 10
n = 2
v = range(n)
l = range(p)
c = range(n)
s = range(p)

# Create the variable names
colnames = ['y111f', 'y111t', 'x11f', 'x11t']

# Create the objective function for the special case with 1 SZ and 1 DZ
obj = [v[0], v[0], 0.0, 0.0]#A v for each y-var, a 0 for each x var

# Create the constraint matrix for the special case with 1 SZ and 1 DZ
rhs = []
constr = []
#Create DZ axis constraints:
rhs += [l[0], l[0]]
constr.append([['x11t'], [1]])
constr.append([['x11f'], [1]])
#Create rectangle length constraints:
rhs += [s[0]]
constr.append([['x11f', 'x11t'], [-1, 1]])
#Create "negative extent rectangle" constraints:
rhs += [0]
constr.append([['x11f', 'x11t'], [1, -1]])
#Linearizing Constraints
rhs += [0, 0]# A zero for each of the x-variables which need to bound the appropriate y variable.
constr.append([['y111f', 'x111f'], [1, -1]])
constr.append([['y111t', 'x111t'], [1, -1]])


# Two demand zones, one supply zone, one demand zone is worth more than the other, they do not overlap.

# Two supply zones and two demand zones which do not overlap. Obvious solution.

### Create the optimization problem for arbitrary inputs
## Create the variable names
#y's, the linearizing surplus vars
colnames = [] 
for j in range(1, n+1):
    for k in range(1, p+1):
        for r in range(1, int(binom(p, k) + 1)):
            colnames.append('y' + str(k) + str(j) + str(r) + 'f')
            colnames.append('y' + str(k) + str(j) + str(r) + 't')
#x's, the original decision vars
for i in range(p):
    for j in range(n):
        colnames.append('x' + str(i) + str(j) + 'f')
        colnames.append('x' + str(i) + str(j) + 't')


## Create the objective function
y_n = int(2*n*sum([binom(p, k) for k in range(1, p+1)]))#how many y vars?
x_n = 2*n*p
obj = list(np.repeat(v, y_n/n)) + [0 for _ in range(x_n)]

## Create the constraints
rhs = []
constr = []
# Don't fall off DZ axes
for i in range(p):
    for j in range(n):
        constr.append([['x' + str(i) + str(j) + 'f'], [1]])
        constr.append([['x' + str(i) + str(j) + 't'], [1]])
        rhs += [l[i], l[i]]
# DZ's must represent possible rectangle
for i in range(p):
    for j in range(n):
        for jp in range(n):
            constr.append([['x' + str(i) + str(j) + 't', 'x' + str(i) + str(jp) + 'f']
                , [1, -1]])
            rhs.append([s[i]])
# No negative extent rectangles
for i in range(n):
    for j in range(p):
        constr.append([['x' + str(i) + str(j) + 't', 'x' + str(i) + str(j) + 'f'],
                [-1, 1]])

## Linearizing constraints, each y has to bound it's corresponding x's
# I've thought of two ways to do this, and I don't know which one I like best yet.
# This way extracts the choices 1 at a time
#for k in range(p):
#    for r in range(1, int(binom(p, k + 1) + 1)):
#        for i in extr_choice(p, k + 1, r):
#            for j in range(n):
#                print k, r, j, i
#                rhs.append([0, 0])
#                constr.append([['x' + str(i) + str(j) + 'f',
#                                'y' + str(k) + str(j) + str(r) + 'f'], [-1, 1]])
#                constr.append([['x' + str(i) + str(j) + 't',
#                                'y' + str(k) + str(j) + str(r) + 't'], [-1, 1]])

# This way enumerates all choices, and chugs through them
for k in range(p):
    for r, choice in enumerate(enum_choices(p, k+1)):
        for i in choice:
            for j in range(n):
                rhs.append([0, 0])
                constr.append([['x' + str(i-1) + str(j) + 'f',
                                'y' + str(k) + str(j) + str(r) + 'f'], [-1, 1]])
                constr.append([['x' + str(i-1) + str(j) + 't',
                                'y' + str(k) + str(j) + str(r) + 't'], [-1, 1]])

# Give how large we expect the constraint matrix to be
const_size = lambda(n, p): n*p*(3 + n + pow(2, p))
print const_size([n, p])
print len(constr)
