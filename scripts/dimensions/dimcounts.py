from math import gcd
from itertools import product
import json, sys

def valid_tuples(n, d):
    """count coefficient tuples (a_1..a_{d-1}, 1) with all signed +-1 combos coprime to n."""
    if n < 2: return 0
    units = [a for a in range(n) if gcd(a, n) == 1]
    if not units: return 0
    signs = [s for s in product((-1,0,1), repeat=d) if any(s)]
    cnt = 0
    for coeff in product(units, repeat=d-1):
        c = coeff + (1,)
        ok = True
        for s in signs:
            if gcd(sum(ci*si for ci,si in zip(c,s)) % n, n) != 1:
                ok = False; break
        if ok: cnt += 1
    return cnt

data = {}
# d=2,3,4 fully; d=5 only the sizes that matter (brute force is heavy at d=5)
ranges = {2: range(2,51), 3: range(2,51), 4: range(2,51), 5: range(2,49)}
for d, R in ranges.items():
    row = []
    for n in R:
        cnt = n * valid_tuples(n, d)   # n offsets k
        row.append([n, cnt])
    data[d] = row
    firsts = [n for n,c in row if c>0][:1]
    print(f"d={d}: first nonzero at n={firsts}, sample {[(n,c) for n,c in row if c>0][:6]}", flush=True)
json.dump(data, open("dimcounts.json","w"))
print("written")
