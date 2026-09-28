import itertools, time, sys
from pysat.solvers import Cadical153
N = 11
V = lambda x, y, z: 1 + x * N * N + y * N + z
inside = lambda p: all(0 <= c < N for c in p)
dirs = [d for d in itertools.product((-1, 0, 1), repeat=3) if d != (0, 0, 0) and d > (0, 0, 0)]  # 13 directions
axis = {(0, 0, 1), (0, 1, 0), (1, 0, 0)}
def lines():
    for d in dirs:
        for p in itertools.product(range(N), repeat=3):
            if inside(tuple(p[i] - d[i] for i in range(3))): continue       # not the start of a line
            line, q = [], p
            while inside(q):
                line.append(q); q = tuple(q[i] + d[i] for i in range(3))
            yield d, line
def build(symmetric):
    cnf = []
    for d, line in lines():
        vs = [V(*p) for p in line]
        if d in axis: cnf.append(vs)                                      # exactly one queen per straight line
        cnf += [[-a, -b] for a, b in itertools.combinations(vs, 2)]       # at most one on any line
    if symmetric:                                                         # third of a turn about the long diagonal
        for x, y, z in itertools.product(range(N), repeat=3):
            a, b = V(x, y, z), V(y, z, x)
            if a < b: cnf += [[-a, b], [a, -b]]
    return cnf
def check(model):
    Q = {p for p in itertools.product(range(N), repeat=3) if model[V(*p) - 1] > 0}
    ok = len(Q) == N * N and all(sum(p in Q for p in line) <= 1 for _, line in lines())
    return Q, ok
for symmetric in (False, True):
    cnf = build(symmetric); t = time.time()
    with Cadical153(bootstrap_with=cnf) as s:
        res = s.solve(); dt = time.time() - t
        label = "with the long-diagonal turn" if symmetric else "any arrangement      "
        if res:
            Q, ok = check(s.get_model())
            sym = all((y, z, x) in Q for x, y, z in Q)
            diag = [p for p in Q if p[0] == p[1] == p[2]]
            print(f"{label}: FOUND in {dt:.1f} s | {len(Q)} queens, valid: {ok}, turn-symmetric: {sym}, queens on the long diagonal: {diag}")
            if symmetric:
                print("heights z for each (x, y), rows = x:")
                H = {(x, y): z for x, y, z in Q}
                for x in range(N): print("   " + " ".join(f"{H[(x, y)]:>2}" for y in range(N)))
        else:
            print(f"{label}: NONE EXISTS (proved by the solver in {dt:.1f} s, {len(cnf):,} clauses)")
    sys.stdout.flush()
