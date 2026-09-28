import itertools, time
from pysat.solvers import Cadical153
def run(N):
    V = lambda p: 1 + p[0] * N * N + p[1] * N + p[2]
    inside = lambda p: all(0 <= c < N for c in p)
    dirs = [d for d in itertools.product((-1, 0, 1), repeat=3) if d > (0, 0, 0)]
    axis = {(0, 0, 1), (0, 1, 0), (1, 0, 0)}
    base = []
    for d in dirs:
        for p in itertools.product(range(N), repeat=3):
            if inside(tuple(p[i] - d[i] for i in range(3))): continue
            line, q = [], p
            while inside(q): line.append(q); q = tuple(q[i] + d[i] for i in range(3))
            vs = [V(c) for c in line]
            if d in axis: base.append(vs)
            base += [[-a, -b] for a, b in itertools.combinations(vs, 2)]
    def apply(perm, flips, p):
        return tuple((N - 1 - p[perm[i]]) if flips[i] else p[perm[i]] for i in range(3))
    def describe(perm, flips):
        inv = sum(perm[i] > perm[j] for i in range(3) for j in range(i + 1, 3))
        rot = (-1) ** (inv + sum(flips)) == 1
        p0 = (0, 1, 3); p, k = apply(perm, flips, p0), 1
        while p != p0: p, k = apply(perm, flips, p), k + 1
        fixed_cells = sum(apply(perm, flips, c) == c for c in itertools.product(range(N), repeat=3))
        if rot:
            name = {2: "half turn", 3: "third of a turn", 4: "quarter turn"}[k]
            if k == 3: where = "about a long diagonal"
            elif k == 4: where = "about an axis"
            else: where = "about an axis" if sum(perm[i] == i for i in range(3)) == 3 else "about a face diagonal"
            return f"{name} {where}"
        if k == 2 and fixed_cells == 1: return "point reflection through the centre"
        if k == 2: return "mirror in a plane"
        return f"turn-and-mirror of order {k}"
    results = {}
    for perm in itertools.permutations(range(3)):
        for flips in itertools.product((0, 1), repeat=3):
            if perm == (0, 1, 2) and flips == (0, 0, 0): continue
            cnf = list(base)
            for c in itertools.product(range(N), repeat=3):
                a, b = V(c), V(apply(perm, flips, c))
                if a != b: cnf += [[-a, b], [a, -b]]
            with Cadical153(bootstrap_with=cnf) as s:
                found = s.solve()
                model = s.get_model() if found else None
            kind = describe(perm, flips)
            results.setdefault(kind, []).append(found)
            if found and kind == "point reflection through the centre":
                Q = [c for c in itertools.product(range(N), repeat=3) if model[V(c) - 1] > 0]
                results.setdefault("_example", Q)
    return results
for N in (11, 13):
    t = time.time(); r = run(N)
    print(f"\n{N}x{N}x{N} complete arrangements ({N*N} queens), all 47 turns and mirrors, {time.time()-t:.1f} s:")
    for kind, fs in sorted((k, v) for k, v in r.items() if not k.startswith("_")):
        print(f"   {kind:38s} x{len(fs):<2}  {'POSSIBLE' if any(fs) else 'impossible (proved)'}")
PY_END=1
