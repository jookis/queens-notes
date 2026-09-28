import itertools
from pysat.solvers import Cadical153
N = 11
V = lambda p: 1 + p[0] * N * N + p[1] * N + p[2]
inside = lambda p: all(0 <= c < N for c in p)
dirs = [d for d in itertools.product((-1, 0, 1), repeat=3) if d > (0, 0, 0)]
axis = {(0, 0, 1), (0, 1, 0), (1, 0, 0)}
cnf, LINES = [], []
for d in dirs:
    for p in itertools.product(range(N), repeat=3):
        if inside(tuple(p[i] - d[i] for i in range(3))): continue
        line, q = [], p
        while inside(q): line.append(q); q = tuple(q[i] + d[i] for i in range(3))
        LINES.append(line); vs = [V(c) for c in line]
        if d in axis: cnf.append(vs)
        cnf += [[-a, -b] for a, b in itertools.combinations(vs, 2)]
flip = lambda p: tuple(N - 1 - c for c in p)
for c in itertools.product(range(N), repeat=3):
    a, b = V(c), V(flip(c))
    if a != b: cnf += [[-a, b], [a, -b]]
with Cadical153(bootstrap_with=cnf) as s:
    assert s.solve(); m = s.get_model()
Q = {c for c in itertools.product(range(N), repeat=3) if m[V(c) - 1] > 0}
valid = len(Q) == N * N and all(sum(c in Q for c in L) <= 1 for L in LINES)
symmetric = all(flip(c) in Q for c in Q)
centre = (N // 2,) * 3 in Q
H = {(x, y): z for x, y, z in Q}
clean = any(all(H[(x, y)] == (a * x + b * y + k) % N for x in range(N) for y in range(N))
            for a in range(N) for b in range(N) for k in range(N))
print(f"{len(Q)} queens | valid: {valid} | unchanged when turned inside out through the centre: {symmetric}")
print(f"queen on the centre square: {centre} | follows the clean rotation rule (any steps, any offset): {clean}")
print("heights z for each (x, y), rows = x:")
for x in range(N): print("   " + " ".join(f"{H[(x, y)]:>2}" for y in range(N)))
