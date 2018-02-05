import numpy as np
from scipy.special import binom

def enum_choices(n, k):
    """
    Enumerate all possible unordered choices of k items from n total items
    """
    current_choice = range(1, k+1)

    combs = [current_choice[:]]
    while current_choice[0] <= n-k:
        for i in range(1, k+1):
            if current_choice[-i] < n - (i - 1):
                current_choice[-i] += 1
                for j in reversed(range(1, i)):
                    current_choice[-j] = current_choice[-(j+1)] + 1
                break
        combs.append(current_choice[:])
    
    return(combs)


def extr_choice(n, k, r):
    """
    Extract the r'th choice which would be enumerated by enum_choices

    Gives the same result as:
    combs = enum_choices(n, k)
    combs[r]
    """
    ai_1 = 0
    a = []
    ra = r
    for i in range(1, k+1):
        # alpha records how many entries share the rightmost i entries with ours
        alpha = np.cumsum([binom(n - ai_1 - j, k - i) for j in range(1, n - ai_1 - k + i + 1)])

        # How many of these "blocks" are we by?
        ind = sum(ra > alpha) 

        # Pad with a zero so we can subtact nothing if desired.
        alpha = [0] + list(alpha)

        # adjust how far down we want to go 
        ra = ra - int(alpha[ind])

        #Record the current entry
        ai = ind + 1 + ai_1
        ai_1 = ai
        
        a.append(ai)

    return(a)

### Test Cases
#ns = [17, 20, 5]
#ks = [3, 10, 2]
#rs = [30, 20, 1]
#
#for i in range(len(ns)):
#    enum = enum_choices(ns[i], ks[i])
#    exact = extr_choice(ns[i], ks[i], rs[i])
#    print(enum[rs[i]-1])
#    print(exact)
