#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  oned_examples.py Author "Nathan Wycoff <nathanbrwycoff@gmail.com>" Date 02.07.2018

# Some tests in 1D
import numpy as np
execfile('form_pmclp_pcr.py')

def number_print(t):
    for i, ii in enumerate(t):
        print(str(i) + ': ' + str(ii))

#For debugging
def sparse_to_vec(s, n):
    rows = []
    for r in s:
        row = [0 for _ in range(n)]
        for i, val in zip(r.ind, r.val):
            row[i] = val
        rows.append(row)

    return(np.array(rows))

sol_vec = np.array(sol)
A = sparse_to_vec(prob.linear_constraints.get_rows(), len(inp['colnames']))
con = sparse_to_vec(prob.linear_constraints.get_rows(), len(inp['colnames'])).dot(sol_vec)

con - inp['rhs']

#################################################################
## One DZ, one SZ, same size. Optimal solution is simply to cover the DZ with the SZ
p = 1
n = 1
v = [1.0]
l = [1.1]
c = [0.2]
s = [1.1]

ret = form_pmclp_pcr_1d(p, n, v, l, c, s)
prob = ret[0]
inp = ret[1]

# Solve the problem.
#The expected answer is x_00t = 0, x_00f = 1.1
expected_sol = [0,1.0,0, 1.1, 1.0]
prob.solve()
val = prob.solution.get_objective_value()
sol = prob.solution.get_values()
x_inds = [a[0] == 'x' for a in ret[1]['colnames']]
x_vals = np.array(sol)[x_inds]

#################################################################
## Two DZ's, one SZ that's big enough to cover both
p = 1
n = 2
v = [1.0, 1.0]
l = [1.1, 2.3]
c = [0.2, 1.5]
s = [3.6]

ret = form_pmclp_pcr_1d(p, n, v, l, c, s)
prob = ret[0]
inp = ret[1]

# Solve the problem, the max value is 3.4
prob.solve()
print(prob.solution.get_objective_value())
sol = prob.solution.get_values()
x_inds = [a[0] == 'x' for a in ret[1]['colnames']]
x_vals = np.array(sol)[x_inds]

#################################################################
## Two DZ's, one SZ that's only big enough to cover one, one is more valuable
## than the other.
p = 1
n = 2
v = [10.0, 1.0]
l = [1.0, 1.0]
c = [0.0, 10.0]
s = [2.0]

ret = form_pmclp_pcr_1d(p, n, v, l, c, s)
prob = ret[0]
inp = ret[1]

prob.solve()
print(prob.solution.get_objective_value())
sol = prob.solution.get_values()
x_inds = [a[0] == 'x' for a in ret[1]['colnames']]
x_vals = np.array(sol)[x_inds]

#################################################################
## Two DZ's, two SZ's, they can each cover each DZ, same value.
p = 2
n = 2
v = [1.0, 1.0]
l = [1.0, 1.0]
c = [0.0, 5.0]
s = [1.0, 1.0]

ret = form_pmclp_pcr_1d(p, n, v, l, c, s)
prob = ret[0]
inp = ret[1]

# Expect x = 0, 1, 0, 1
prob.solve()
print(prob.solution.get_objective_value())
sol = prob.solution.get_values()
x_inds = [a[0] == 'x' for a in ret[1]['colnames']]
x_vals = np.array(sol)[x_inds]

#################################################################
## One DZ's and two SZ's. They can each cover half of the DZ.
p = 2
n = 1
v = [1.0]
l = [2.0]
c = [0.1]
s = [1.0, 1.0]

ret = form_pmclp_pcr_1d(p, n, v, l, c, s)
prob = ret[0]
inp = ret[1]

# Val should be 2.0
possible_sol = [0,1,-1,2,-1,1,0,1,1,2,1,1]#Double check
prob.solve()
print(prob.solution.get_objective_value())
sol = prob.solution.get_values()
x_inds = [a[0] == 'x' for a in ret[1]['colnames']]
x_vals = np.array(sol)[x_inds]

# Write out the problematic problem
prob.write("oneAtwoB.lp")

#################################################################
## Two DZ's and two SZ's. They can cover each other perfectly, but one DZ is
## much more valuable than the other (tests that double coverage is not counted).

p = 2
n = 2
v = [10.0, 1.0]
l = [1.0, 1.0]
c = [0.0, 2.0]
s = [1.0, 1.0]

ret = form_pmclp_pcr_1d(p, n, v, l, c, s)
prob = ret[0]
inp = ret[1]

# Val should be 11
prob.solve()
print(prob.solution.get_objective_value())
expected_sol = 
sol = prob.solution.get_values()
