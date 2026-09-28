import sys, time
from nonclean_lib import build, add_nonclean
from pysat.solvers import Solver
N = 13
cnf, Q = build(N); add_nonclean(N, cnf, Q, N ** 3 + 1)
t = time.time()
with Solver(name=sys.argv[1], bootstrap_with=cnf) as s:
    r = s.solve(); m = s.get_model() if r else None
print(f"{sys.argv[1]}: {'FOUND a non-clean 13x13x13 cube' if r else 'NONE EXISTS (proved)'} after {time.time() - t:.0f} s", flush=True)
if r:
    H = {(x, y): z for x in range(N) for y in range(N) for z in range(N) if m[Q(x, y, z) - 1] > 0}
    for x in range(N): print(" ".join(f"{H[(x, y)]:>2}" for y in range(N)))
