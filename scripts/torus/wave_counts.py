from math import gcd
def primes(n): return [p for p in range(2, n + 1) if n % p == 0 and all(p % q for q in range(2, p))]
def brute_cube(n):     # step pairs (a, b) where no line in the 13 directions surfs the wave
    u = lambda v: gcd(v % n, n) == 1
    return sum(all(u(v) for v in (a, b, a - 1, a + 1, b - 1, b + 1, a + b, a - b, a + b - 1, a + b + 1, a - b - 1, a - b + 1))
               for a in range(n) for b in range(n))
def formula_cube(n):
    r = n * n
    for p in primes(n): r = r * (p - 5) * (p - 7) // (p * p)
    return r
print(" n    wave pairs (a,b)   formula   clean cubes")
for n in [n for n in range(2, 150) if gcd(n, 210) == 1]:
    b, f = brute_cube(n), formula_cube(n)
    print(f"{n:3}   {b:10}      {f:8}   {n * b:10,}   {'ok' if b == f else 'MISMATCH'}")
def is_solution(c):
    n = len(c)
    return len(set(c)) == n and len({r + c[r] for r in range(n)}) == n and len({r - c[r] for r in range(n)}) == n
ok = [n for n in range(4, 2001) if n % 6 not in (2, 3) and is_solution(list(range(1, n, 2)) + list(range(0, n, 2)))]
print(f"flat board, two step-2 waves (odd columns then even): works for {len(ok)} of the "
      f"{sum(1 for n in range(4, 2001) if n % 6 not in (2, 3))} sizes 4..2000 with n mod 6 not 2 or 3")
