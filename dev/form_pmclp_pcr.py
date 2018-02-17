#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  form_pmclp_pcr.py Author "Nathan Wycoff <nathanbrwycoff@gmail.com>" Date 02.07.2018

'''
Formulate the linear program representation of the one dimensional Planar Maximum Coverage Location Problem with Partial Coverage and Rectangular Demand Zones, for use with the CPLEX python module.
'''

#TODO: just import cplex
#import sys
#sys.path.append('/home/nathw95/python_paks/pkgs/cplex/lib/python/')
import cplex

#TODO: Probably just fold this in at some point
execfile('comb_funcs.py')

def form_pmclp_pcr_1d(p, n, v, l, c, s):
    """
    Formulate the PMCLP-PCR problem for one dimensional problems. See Bansal and Kianfar (2017) for more info.

    arg  p: The number of Supply Zones
    type p: int

    arg  n: The number of Demand Zones
    type n: int

    arg  v: The weight of each Demand Zone
    type v: A list of length n

    arg  l: The length of each Demand Zone
    type l: A list of length n

    arg  c: The leftmost point belonging to each demand zone (beginning of each demand zone).
    type c: A list of length n

    arg  s: The length of each Supply Zone
    type s: A list of length p
    """

    #TODO: c should be scaled such that its minimum value is 0

    ## Create the variable names
    #y's, the objective linearizing surplus vars
    colnames = [] 
    for j in range(n):
        for k in range(p):
            for r in range(int(binom(p, k + 1))):
                colnames.append('y' + str(k) + str(j) + str(r) + 'f')
                colnames.append('y' + str(k) + str(j) + str(r) + 't')
    #z's, the constraint linearizing surplus vars
    for i in range(p):
        colnames.append('z' + str(i) + 'f')
        colnames.append('z' + str(i) + 't')
    #x's, the original decision vars
    for i in range(p):
        for j in range(n):
            colnames.append('x' + str(i) + str(j) + 'f')
            colnames.append('x' + str(i) + str(j) + 't')

    ## Create the variable bounds
    y_n = int(2*n*sum([binom(p, k) for k in range(1, p+1)]))#how many y vars?
    z_n = 2*p
    x_n = 2*n*p
    #x's and y...t's are in [0,infty), while y...f's are in (-infty, 0]
    lb = [-cplex.infinity if i % 2 == 0 else 0 for i in range(y_n)] + \
            [-cplex.infinity if i % 2 == 0 else 0 for i in range(z_n)] + \
            [0 for _ in range(x_n)]
    ub = [0 if i % 2 == 0 else cplex.infinity for i in range(y_n)] + \
            [0 if i % 2 == 0 else cplex.infinity for i in range(z_n)] + \
            [cplex.infinity for _ in range(x_n)]


    ## Create the objective function
    obj = list(np.repeat(v, y_n/n)) + [0 for _ in range(z_n + x_n)]

    ## Create the linear constraints
    lin_rhs = []
    lin_constr = []
    quad_constr = []
    qlin_constr = []
    quad_rhs = []

    # Don't fall off DZ axes
    for i in range(p):
        for j in range(n):
            lin_constr.append([['x' + str(i) + str(j) + 'f'], [1]])#TODO: Probably redundatnt
            lin_constr.append([['x' + str(i) + str(j) + 't'], [1]])
            lin_rhs += [l[j], l[j]]

    # DZ's must represent possible rectangle
    for i in range(p):
        for j in range(n):
            for jp in range(n):
                quad_constr.append(cplex.SparseTriple(
                    ['x' + str(i) + str(j) + 'f', 'x' + str(i) + str(j) + 'f'],
                    ['x' + str(i) + str(j) + 'f', 'x' + str(i) + str(jp) + 't'],
                    [-1, 1]))
                qlin_constr.append(cplex.SparsePair(
                    ['x' + str(i) + str(j) + 'f'], [c[jp] - c[j] - s[i]]))
                quad_rhs.append(0)

    #The old linear attempt; does not seem to work.
    #for i in range(p):
    #    lin_constr.append([['z' + str(i) + 't', 'z' + str(i) + 'f'], [1, 1]])
    #    lin_rhs.append(s[i])
    #    for j in range(n):
    #        lin_constr.append([['z' + str(i) + 't', 'x' + str(i) + str(j) + 't'], [-1, 1]])
    #        lin_constr.append([['z' + str(i) + 'f', 'x' + str(i) + str(j) + 'f'], [-1, -1]])
    #        lin_rhs.append(-c[j])
    #        lin_rhs.append(c[j])
    # No negative extent rectangles
    for i in range(p):
        for j in range(n):
            lin_rhs.append(0)
            lin_constr.append([['x' + str(i) + str(j) + 't', 'x' + str(i) + str(j) + 'f'],
                    [-1, 1]])

    ## Linearizing lin_constraints, each y has to bound it's corresponding x's
    # I've thought of two ways to do this, and I don't know which one I like best yet.
    # This way extracts the choices 1 at a time
    #for k in range(p):
    #    for r in range(1, int(binom(p, k + 1) + 1)):
    #        for i in extr_choice(p, k + 1, r):
    #            for j in range(n):
    #                print k, r, j, i
    #                lin_rhs.append([0, 0])
    #                lin_constr.append([['x' + str(i) + str(j) + 'f',
    #                                'y' + str(k) + str(j) + str(r) + 'f'], [-1, 1]])
    #                lin_constr.append([['x' + str(i) + str(j) + 't',
    #                                'y' + str(k) + str(j) + str(r) + 't'], [-1, 1]])

    # This way enumerates all choices, and chugs through them
    for k in range(p):
        for r, choice in enumerate(enum_choices(p, k+1)):
            for i in choice:
                for j in range(n):
                    lin_rhs.extend([0, 0])
                    lin_constr.append([['x' + str(i-1) + str(j) + 'f',
                                    'y' + str(k) + str(j) + str(r) + 'f'], [1, 1]])
                    lin_constr.append([['x' + str(i-1) + str(j) + 't',
                                    'y' + str(k) + str(j) + str(r) + 't'], [-1, 1]])

    ## Give these objects to CPLEX to create a CPLEX problem.
    prob = cplex.Cplex()

    try:
        lin_senses = ''.join('L' for _ in range(len(lin_constr)))
        quad_senses = ['L' for _ in range(len(quad_constr))]

        # Init problem and add linear constraints
        prob.objective.set_sense(prob.objective.sense.maximize)
        prob.variables.add(obj=obj, names=colnames, lb = lb, 
                ub = ub)
        prob.linear_constraints.add(lin_expr=lin_constr, 
                rhs=lin_rhs, senses = lin_senses)

        # Add quadratic constraints
        for q in range(len(quad_constr)):
            prob.quadratic_constraints.add(lin_expr = qlin_constr[q],
                                        quad_expr = quad_constr[q],
                                        sense = quad_senses[q],
                                        rhs = quad_rhs[q])
    except Exception as e:
        print("Whoops, the problem couldn't be created")
        print(e)


    ## Prepare a dict with the results
    ret = {}
    ret['colnames'] = colnames
    ret['lb'] = lb
    ret['ub'] = ub
    ret['obj'] = obj
    ret['lin_rhs'] = lin_rhs
    ret['lin_constr'] = lin_constr
    return [prob, ret]
