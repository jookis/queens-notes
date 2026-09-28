from math import gcd
from itertools import product

def works(n, d):
    """Is there a clean linear wave arrangement on the d-dim torus of side n?
    Coefficients (a_1..a_{d-1}, and 1 for the dependent axis); need every signed
    +-1 combination of them (nonzero pattern) to be coprime to n."""
    signs = [s for s in product((-1,0,1), repeat=d) if any(s)]   # (3^d-1) direction patterns
    units = [a for a in range(n) if gcd(a, n) == 1]
    if not units and n > 1:
        return False
    # brute force the d-1 free coefficients; the last coefficient is fixed at 1
    for coeff in product(units if units else [0], repeat=d-1):
        c = coeff + (1,)
        ok = True
        for s in signs:
            v = sum(ci*si for ci, si in zip(c, s)) % n
            if gcd(v, n) != 1:
                ok = False; break
        if ok:
            return True
    return False

def primorial_upto(x):
    P = 1
    for p in range(2, x+1):
        if all(p % q for q in range(2, p)):
            P *= p
    return P

for d in (2, 3, 4):
    good, bad = [], []
    hi = 30 if d == 4 else 45
    for n in range(2, hi+1):
        (good if works(n, d) else bad).append(n)
    # find the smallest modulus M such that "good == coprime to M"
    forbidden_primes = sorted({p for n in bad for p in range(2, n+1)
                               if n % p == 0 and all(p % q for q in range(2, p))
                               and not works(p, d)})
    M = 1
    for p in forbidden_primes: M *= p
    match = all((works(n, d) == (gcd(n, M) == 1)) for n in range(2, hi+1))
    print(f"{d}D: good sizes {good[:14]}{'...' if len(good)>14 else ''}")
    print(f"    forbidden primes {forbidden_primes}, product {M}, "
          f"'good == coprime to {M}' holds up to {hi}: {match}")
    print(f"    2^{d}-1 = {2**d-1}, primorial up to that = {primorial_upto(2**d-1)}")
