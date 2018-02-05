#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  cplex_example.py Author "Nathan Wycoff <nathanbrwycoff@gmail.com>" Date 01.31.2018

## An extremely basic example just so i gain an understanding of how to interface with CPLEX.

## Here's the module load commands I use, I should get rid of these someday
#TODO: Get rid of these
module load Anaconda cplex

#Since I have built the cplex module in a nonstandard location, I need to add it to the path
#in order to load the module
import sys
sys.path.append('/home/nathw95/python_paks/pkgs/cplex/lib/python/')
import cplex

## I'm going to try to optimize 2*x1 + x2
## s.t. x1 + x2 <= 10
##      2x1 + 2/3 x2 <= 13

# data common to all populateby functions
my_obj = [2, 1]
my_rhs = [10, 13]
m = 2
my_colnames = ['x' + str(i + 1) for i in range(m)]
my_rownames = ['c' + str(i + 1) for i in range(m)]
my_sense = "LL"

prob = cplex.Cplex()

mat = [[1,2], [2, 2.0/3.0]]
rows = [[range(m), x] for x in mat]

# Store things in the cplex object.
prob.objective.set_sense(prob.objective.sense.maximize)
prob.variables.add(obj=my_obj, names=my_colnames)
prob.linear_constraints.add(lin_expr=rows, senses=my_sense,
                            rhs=my_rhs, names=my_rownames)

# Solve the problem.
prob.solve()
print("Solution status = ", prob.solution.get_status(), ":")
print("Solution value  = ", prob.solution.get_objective_value())
