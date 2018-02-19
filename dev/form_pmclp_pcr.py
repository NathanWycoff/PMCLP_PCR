#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  form_pmclp_pcr.py Author "Nathan Wycoff <nathanbrwycoff@gmail.com>" Date 02.07.2018

'''
Formulate the linear program representation of the one dimensional Planar Maximum Coverage Location Problem with Partial Coverage and Rectangular Demand Zones, for use with the CPLEX python module.
'''

#TODO: just import cplex
import sys
sys.path.append('/home/nathw95/python_paks/pkgs/cplex/lib/python/')
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

    ## Create the variable names
    #y's, the linearizing surplus vars
    colnames = [] 
    for j in range(n):
        for k in range(p):
            for r in range(int(binom(p, k + 1))):
                colnames.append('y' + str(k) + str(j) + str(r) + 'f')
                colnames.append('y' + str(k) + str(j) + str(r) + 't')
    #x's, the original decision vars
    for i in range(p):
        for j in range(n):
            colnames.append('x' + str(i) + str(j) + 'f')
            colnames.append('x' + str(i) + str(j) + 't')
    #b's, binary variables linearizing the rectangle constraint
    bin_vars = []
    for i in range(p):
        for j in range(n):
            for jp in range(n):
                bin_vars.append('b' + str(i) + str(j) + str(jp))
    colnames += bin_vars

    ## Create the variable bounds
    y_n = int(2*n*sum([binom(p, k) for k in range(1, p+1)]))#how many y vars?
    x_n = 2*n*p
    b_n = p*n*n
    #x's and y...t's are in [0,infty), while y...f's are in (-infty, 0]. The b's are binary.
    lb = [-cplex.infinity if i % 2 == 0 else 0 for i in range(y_n)] + \
            [0 for _ in range(x_n)] + \
            [0 for _ in range(b_n)]
    ub = [0 if i % 2 == 0 else cplex.infinity for i in range(y_n)] + \
            [cplex.infinity for _ in range(x_n)] + \
            [1 for _ in range(b_n)]



    ## Create the objective function
    #TODO: Don't count double coverage
    obj = list(np.repeat(v, y_n/n)) + [0 for _ in range(x_n)] + [0 for _ in range(b_n)]

    ## Create the constraints
    rhs = []
    constr = []
    # Don't fall off DZ axes
    for i in range(p):
        for j in range(n):
            constr.append([['x' + str(i) + str(j) + 'f'], [1]])
            constr.append([['x' + str(i) + str(j) + 't'], [1]])
            rhs += [l[j], l[j]]
    # DZ's must represent possible rectangle
    dim_range = max([c[i] + l[i] for i in range(n)]) - min(c)
    for i in range(p):
        for j in range(n):
            for jp in range(n):
                ## Build constraints on the binary variable in order to achieve a conditional constraint
                # Constrain it to be less than both x vars, so if either is zero, it will be zero
                #constr.append([['x' + str(i) + str(j) + 'f', \
                #    'b' + str(i) + str(j) + str(jp)], [-1, 1]])
                constr.append([['x' + str(i) + str(jp) + 't', \
                        'b' + str(i) + str(j) + str(jp)], [-1, 1]])
                rhs += [0]
                # Constrain it to be greater than or equal to each x var divided by the extent of it's rectangle
                # This will constrain it to be 1 if either one or both of is positive.
                #constr.append([['x' + str(i) + str(j) + 'f', \
                        #'b' + str(i) + str(j) + str(jp)], [1, -l[j]]])
                constr.append([['x' + str(i) + str(jp) + 't', \
                        'b' + str(i) + str(j) + str(jp)], [1, -l[jp]]])
                rhs += [0]

                ## Add the actual desired constraint: if both x vars are positive, they can only be so far apart.
                constr.append([['x' + str(i) + str(j) + 'f', \
                        'x' + str(i) + str(jp) + 't', \
                        'b' + str(i) + str(j) + str(jp)], [-1, 1, dim_range]])
                rhs += [-c[jp] + c[j] + s[i] + dim_range]
    # No negative extent rectangles
    for i in range(p):
        for j in range(n):
            rhs.append(0)
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
                    rhs.extend([0, 0])
                    constr.append([['x' + str(i-1) + str(j) + 'f',
                                    'y' + str(k) + str(j) + str(r) + 'f'], [1, 1]])
                    constr.append([['x' + str(i-1) + str(j) + 't',
                                    'y' + str(k) + str(j) + str(r) + 't'], [-1, 1]])

    ## Give these objects to CPLEX to create a CPLEX problem.
    prob = cplex.Cplex()

    try:
        senses = ''.join('L' for _ in range(len(constr)))

        prob.objective.set_sense(prob.objective.sense.maximize)
        prob.variables.add(obj=obj, names=colnames, lb = lb, 
                ub = ub)
        prob.linear_constraints.add(lin_expr=constr, rhs=rhs, senses = senses)

        for var in bin_vars:
            prob.variables.set_types(var, prob.variables.type.binary)
    except Exception as e:
        print("Whoops, the problem couldn't be created")
        print(e)


    ## Prepare a dict with the results
    ret = {}
    ret['colnames'] = colnames
    ret['lb'] = lb
    ret['ub'] = ub
    ret['obj'] = obj
    ret['rhs'] = rhs
    ret['constr'] = constr
    return [prob, ret]
