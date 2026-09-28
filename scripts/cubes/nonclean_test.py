import itertools
from nonclean_lib import add_nonclean
from pysat.solvers import Glucose4
N = 11
Q = lambda x, y, z: 1 + x * N * N + y * N + z
def accepts(H):
    cnf = []; add_nonclean(N, cnf, Q, N ** 3 + 1)
    cnf += [[Q(x, y, z)] if H[(x, y)] == z else [-Q(x, y, z)] for x in range(N) for y in range(N) for z in range(N)]
    with Glucose4(bootstrap_with=cnf) as s: return s.solve()
clean = [(a, b, k) for a in range(N) for b in range(N) for k in range(N)]
rejected = sum(not accepts({(x, y): (a * x + b * y + k) % N for x in range(N) for y in range(N)}) for a, b, k in clean)
print(f"clean arrangements (all {len(clean)} of the form a*x + b*y + k): rejected {rejected}/{len(clean)}  (must be all)")
base = {(x, y): (2 * x + 4 * y + 8) % N for x in range(N) for y in range(N)}
changed = 0
for cell in [(0, 0), (5, 7), (10, 10), (3, 0), (0, 9)]:
    H = dict(base); H[cell] = (H[cell] + 1) % N; changed += accepts(H)
print(f"clean cube with one square's height altered: accepted {changed}/5  (must be all)")
order = [0, 2, 1, 3, 4, 5, 6, 7, 8, 9, 10]                       # non-staircase stacking of step-2 floors
H = {(x, (2 * x + c) % N): z for z, c in enumerate(order) for x in range(N)}
print(f"step-2 floors stacked out of staircase order: accepted {accepts(H)}  (must be True)")
