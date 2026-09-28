from math import gcd
from itertools import product

def valid(n, d, coeffs):
    """coeffs = the d coefficients (dependent axis included); check the clean-wave condition."""
    for s in product((-1,0,1), repeat=d):
        if any(s) and gcd(sum(c*si for c,si in zip(coeffs,s)) % n, n) != 1:
            return False
    return True

def coprime_to_primorial(n, d):
    return all(n % p or p >= 2**d for p in range(2, n+1)
               if all(p % q for q in range(2, p)))

for d in (2,3,4):
    powers = [2**i for i in range(d)]     # 1,2,4,...,2^(d-1): the "binary" coefficients
    hits, misses = [], []
    for n in range(2, 60):
        good_by_rule = coprime_to_primorial(n, d)
        works_powers = valid(n, d, powers)
        if good_by_rule == works_powers:
            (hits if good_by_rule else hits).append(n)
        else:
            misses.append(n)
    ok = [n for n in range(2,60) if valid(n,d,powers)]
    print(f"{d}D, coefficients {powers}: clean solution for n = {ok}")
    print(f"    matches 'n coprime to all primes below {2**d}' for every n<60: {not misses}")
