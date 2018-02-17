#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  oned_examples.py Author "Nathan Wycoff <nathanbrwycoff@gmail.com>" Date 02.07.2018

# Some tests in 1D
execfile('form_pmclp_pcr.py')

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
prob.solve()
sol = prob.solution.get_values()
x_vals = sol[-(2*n*p):]

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
prob.solution.get_objective_value()
sol = prob.solution.get_values()
x_vals = sol[-(2*n*p):]

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

# Expect it to only cover the first zone, givin us [0, 1, 0, 0] and a value of 10.0
prob.solve()
prob.solution.get_objective_value()
sol = prob.solution.get_values()
x_vals = sol[-(2*n*p):]

#################################################################
## Two DZ's and two SZ's. They can cover each other perfectly, but one DZ is
## much more valuable than the other (tests that double coverage is not counted).

#TODO: This doesn't work yet, it would seem that I am going to need slack variables for the "map back to rectangles" constraint, but I need to think some more about it.
p = 2
n = 2
v = [10.0, 1.0]
l = [1.0, 1.0]
c = [0.0, 2.0]
s = [1.0, 1.0]

ret = form_pmclp_pcr_1d(p, n, v, l, c, s)
prob = ret[0]
inp = ret[1]

# Solve the problem, the max value is 3.4
prob.solve()
prob.solution.get_objective_value()
sol = prob.solution.get_values()
x_vals = sol[-(2*n*p):]
