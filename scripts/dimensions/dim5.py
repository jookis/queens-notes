from math import gcd
from itertools import product

def valid(n, d, coeffs):
    return all(gcd(sum(c*si for c,si in zip(coeffs,s)) % n, n) == 1
               for s in product((-1,0,1), repeat=d) if any(s))

def exhaustive(n, d):
    units = [a for a in range(n) if gcd(a,n)==1]
    return any(valid(n, d, coeff+(1,)) for coeff in product(units, repeat=d-1))

def coprime_primes_below(n, bound):
    return all(n % p or p >= bound for p in range(2,n+1) if all(p%q for q in range(2,p)))

d = 5
powers = [2**i for i in range(d)]           # 1,2,4,8,16
print(f"5D, binary coefficients {powers}, boundary predicts: avoid primes below 2^5 = 32")
good = [n for n in range(2,64) if valid(n, d, powers)]
print(f"  construction works for n = {good}")
print(f"  matches 'n coprime to every prime below 32' up to 63: "
      f"{all(valid(n,d,powers)==coprime_primes_below(n,32) for n in range(2,64))}")
# necessity: no coefficients at all work for the small forbidden sizes (exhaustive, small n only)
small = {n: exhaustive(n, d) for n in range(2,25)}
print(f"  exhaustive n<25, any coefficients work: {[n for n,v in small.items() if v]}")
print(f"  primorial of primes below 32 = {__import__('math').prod([p for p in range(2,32) if all(p%q for q in range(2,p))])}")
