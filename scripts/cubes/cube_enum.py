import itertools, time, sys
from pysat.solvers import Glucose4
def enumerate_cubes(N, budget):
    V = lambda p: 1 + p[0] * N * N + p[1] * N + p[2]
    inside = lambda p: all(0 <= c < N for c in p)
    dirs = [d for d in itertools.product((-1, 0, 1), repeat=3) if d > (0, 0, 0)]
    axis = {(0, 0, 1), (0, 1, 0), (1, 0, 0)}
    cnf, lines = [], []
    for d in dirs:
        for p in itertools.product(range(N), repeat=3):
            if inside(tuple(p[i] - d[i] for i in range(3))): continue
            line, q = [], p
            while inside(q): line.append(q); q = tuple(q[i] + d[i] for i in range(3))
            lines.append(line); vs = [V(c) for c in line]
            if d in axis: cnf.append(vs)
            cnf += [[-a, -b] for a, b in itertools.combinations(vs, 2)]
    cubes, proven, t0 = [], False, time.time()
    with Glucose4(bootstrap_with=cnf) as s:
        while time.time() - t0 < budget:
            s.conf_budget(20000)
            r = s.solve_limited()
            if r is None: continue                      # budget slice used up; learned clauses are kept
            if r is False: proven = True; break         # no further cube exists
            m = s.get_model()
            cube = [p for p in itertools.product(range(N), repeat=3) if m[V(p) - 1] > 0]
            cubes.append(cube)
            s.add_clause([-V(p) for p in cube])
    return cubes, proven, time.time() - t0, lines
def report(N, budget):
    cubes, proven, dt, lines = enumerate_cubes(N, budget)
    ok = lambda cube: (len(cube) == N * N and
                       all(sum(1 for p in L if p in set_) <= 1 for L in lines) if (set_ := set(cube)) else False)
    def clean(cube):
        H = {(x, y): z for x, y, z in cube}
        k = H[(0, 0)]; a = (H[(1, 0)] - k) % N; b = (H[(0, 1)] - k) % N
        return all(H[(x, y)] == (a * x + b * y + k) % N for x in range(N) for y in range(N))
    tilings = {}
    for cube in cubes:
        floors = [tuple(y for x in range(N) for (xx, y, zz) in cube if xx == x and zz == z) for z in range(N)]
        key = frozenset(floors)
        diffs = {(floors[z + 1][0] - floors[z][0]) % N for z in range(N - 1)}
        shift = sorted(diffs)[0] if len(diffs) == 1 else "irregular"
        steps = frozenset((f[1] - f[0]) % N for f in floors)
        e = tilings.setdefault(key, {"steps": steps, "orders": 0, "shifts": {}})
        e["orders"] += 1; e["shifts"][shift] = e["shifts"].get(shift, 0) + 1
    print(f"\n=== {N}x{N}x{N}: {len(cubes)} complete cubes, "
          f"{'PROVEN to be all of them' if proven else 'search budget ran out, may be more'} ({dt:.0f} s)")
    print(f"{'layer step':>11} {'stacking orders':>16}   shifts per floor")
    for e in sorted(tilings.values(), key=lambda e: sorted(e["steps"])):
        st = str(sorted(e["steps"])[0]) if len(e["steps"]) == 1 else "mixed " + str(sorted(e["steps"]))
        print(f"{st:>11} {e['orders']:>16}   " + ", ".join(f"{k}: {v}" for k, v in sorted(e["shifts"].items(), key=lambda kv: str(kv[0]).zfill(3))))
    print(f"tilings that stack: {len(tilings)} | cubes passing the independent check: {sum(ok(c) for c in cubes)} | following the clean rule: {sum(clean(c) for c in cubes)}")
    sys.stdout.flush()
report(11, 150)
report(13, 330)
