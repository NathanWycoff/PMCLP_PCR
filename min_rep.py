#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  min_rep.py Author "Nathan Wycoff <nathanbrwycoff@gmail.com>" Date 05.17.2018

## A minimal example reproducing the observed issue.

import cplex
import numpy as np

prob = cplex.Cplex("oneAtwoB.lp")

# Check CPLEX solution.
prob.solve()
print(prob.solution.get_objective_value())
sol = prob.solution.get_values()
print sol

#For debugging, convert CPLEX's sparse format into a dense numpy array.
def sparse_to_vec(s, n):
    rows = []
    for r in s:
        row = [0 for _ in range(n)]
        for i, val in zip(r.ind, r.val):
            row[i] = val
        rows.append(row)

    return(np.array(rows))

# Try our own solution.
possible_sol = [0,1,-1,2,-1,1,0,1,1,2,1,1]#Double check

sol_vec = np.array(possible_sol)
var_names = prob.variables.get_names()
A = sparse_to_vec(prob.linear_constraints.get_rows(), len(var_names))
con = A.dot(sol_vec)

print con - prob.linear_constraints.get_rhs()
