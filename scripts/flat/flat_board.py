"""Flat-board checks: counts, symmetry families, the 8x8 overlay, and why 8x8x8 has no complete cube.

    python3 flat_board.py          # a few seconds

A solution is a tuple s where s[row] = column.
"""
import itertools

def solutions(n, torus=False):
    out = []
    def go(r, cols, d1, d2, s):
        if r == n:
            out.append(tuple(s)); return
        for c in range(n):
            a, b = (r - c) % n if torus else r - c, (r + c) % n if torus else r + c
            if c in cols or a in d1 or b in d2: continue
            s.append(c); go(r + 1, cols | {c}, d1 | {a}, d2 | {b}, s); s.pop()
    go(0, frozenset(), frozenset(), frozenset(), [])
    return out

def rot90(s):
    n = len(s); t = [0] * n
    for r, c in enumerate(s): t[c] = n - 1 - r
    return tuple(t)

def symmetries(s):
    out, t = [], s
    for _ in range(4):
        out += [t, tuple(reversed(t))]
        t = rot90(t)
    return out

print(" n   flat   doughnut   families   same after half turn   same after quarter turn")
for n in range(4, 13):
    flat = solutions(n)
    tor = len(solutions(n, torus=True))
    fam = len({min(symmetries(s)) for s in flat})
    half = sum(rot90(rot90(s)) == s for s in flat)
    quarter = sum(rot90(s) == s for s in flat)
    print(f"{n:2d} {len(flat):6d} {tor:9d} {fam:9d} {half:14d} {quarter:22d}")

sols8 = solutions(8)
print("\n8x8: all 92 solutions stacked on one board (queens per square):")
grid = [[0] * 8 for _ in range(8)]
for s in sols8:
    for r, c in enumerate(s): grid[r][c] += 1
for row in grid: print("  " + " ".join(f"{v:2d}" for v in row))

shared = max(sum(a[r] == b[r] for r in range(8)) for a, b in itertools.combinations(sols8, 2))
print(f"\nclosest two distinct 8x8 solutions share {shared} of 8 queens")

# A complete 8x8x8 cube would need 8 flat solutions (its floors) with no square in common.
sq = [frozenset(enumerate(s)) for s in sols8]
best = 0
def grow(chosen, start):
    global best
    best = max(best, len(chosen))
    if best == 8: return
    for i in range(start, len(sq)):
        if all(sq[i].isdisjoint(sq[j]) for j in chosen): grow(chosen + [i], i + 1)
grow([], 0)
print(f"largest set of 8x8 solutions with no shared square: {best} (a complete 8x8x8 cube needs 8)")

# Blow-up products: every queen of the big pattern A becomes a copy of the tile B.
def product(a, b):
    m = len(b)
    return tuple(a[r // m] * m + b[r % m] for r in range(len(a) * m))

def valid(s):
    n = len(s)
    return len(set(s)) == n and len({r - c for r, c in enumerate(s)}) == n and len({r + c for r, c in enumerate(s)}) == n

sols5 = solutions(5)
print("\nproducts (big pattern x tile):")
for name, A, B in (("8 x 5", sols8, sols5), ("5 x 8", sols5, sols8)):
    ok = sum(valid(product(a, b)) for a in A for b in B)
    print(f"  {name}: {ok} of {len(A) * len(B)} valid")
