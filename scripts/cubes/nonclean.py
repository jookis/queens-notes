import itertools, time, sys
from pysat.solvers import Glucose4
def build(N, cross_layer=True):
    """Complete-cube constraints. cross_layer=False keeps only rules inside each floor plus one queen
    per vertical column: a deliberately looser puzzle, used to check the encoding is not vacuous."""
    Q = lambda x, y, z: 1 + x * N * N + y * N + z
    inside = lambda p: all(0 <= c < N for c in p)
    dirs = [d for d in itertools.product((-1, 0, 1), repeat=3) if d > (0, 0, 0)]
    if not cross_layer: dirs = [d for d in dirs if d[2] == 0] + [(0, 0, 1)]
    axis = {(0, 0, 1), (0, 1, 0), (1, 0, 0)}
    cnf = []
    for d in dirs:
        for p in itertools.product(range(N), repeat=3):
            if inside(tuple(p[i] - d[i] for i in range(3))): continue
            line, q = [], p
            while inside(q): line.append(q); q = tuple(q[i] + d[i] for i in range(3))
            vs = [Q(*c) for c in line]
            if d in axis: cnf.append(vs)
            cnf += [[-a, -b] for a, b in itertools.combinations(vs, 2)]
    # "not clean": some neighbouring columns differ in height by something other than the reference step
    nxt = [N ** 3 + 1]
    def new():
        nxt[0] += 1; return nxt[0] - 1
    def diff_vars(c1, c2):
        D = [new() for _ in range(N)]                 # D[delta] true iff height(c2) - height(c1) == delta mod N
        for z in range(N):
            for dlt in range(N):
                cnf.append([-Q(*c1, z), -Q(*c2, (z + dlt) % N), D[dlt]])
                cnf.append([-D[dlt], -Q(*c1, z), Q(*c2, (z + dlt) % N)])
        return D
    A = diff_vars((0, 0), (1, 0)); B = diff_vars((0, 0), (0, 1))
    witnesses = []
    for x in range(N):
        for y in range(N):
            for (c2, R) in ((((x + 1, y)), A), (((x, y + 1)), B)):
                if not inside((*c2, 0)) or ((x, y) == (0, 0) and c2 in ((1, 0), (0, 1))): continue
                D = diff_vars((x, y), c2)
                for dlt in range(N):
                    w = new(); witnesses.append(w)
                    cnf.append([-w, D[dlt]]); cnf.append([-w, -R[dlt]])
    cnf.append(witnesses)
    return cnf
def ask(label, N, cross_layer, budget):
    cnf = build(N, cross_layer); t0 = time.time(); res = None
    with Glucose4(bootstrap_with=cnf) as s:
        while time.time() - t0 < budget:
            s.conf_budget(50000)
            r = s.solve_limited()
            if r is not None: res = r; break
    verdict = {True: "FOUND one", False: "NONE EXISTS (proved)", None: "undecided (budget ran out)"}[res]
    print(f"{label}: {verdict}  [{time.time() - t0:.0f} s, {len(cnf):,} clauses]"); sys.stdout.flush()
ask("sanity, looser puzzle at 11, a non-clean arrangement", 11, False, 30)
ask("complete 11x11x11 cube that is NOT clean            ", 11, True, 60)
ask("complete 13x13x13 cube that is NOT clean            ", 13, True, 420)
