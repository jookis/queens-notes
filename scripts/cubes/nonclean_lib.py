import itertools
def build(N):
    """All complete-cube constraints: one queen per straight line, at most one on any diagonal line."""
    Q = lambda x, y, z: 1 + x * N * N + y * N + z
    inside = lambda p: all(0 <= c < N for c in p)
    axis = {(0, 0, 1), (0, 1, 0), (1, 0, 0)}
    cnf = []
    for d in (d for d in itertools.product((-1, 0, 1), repeat=3) if d > (0, 0, 0)):
        for p in itertools.product(range(N), repeat=3):
            if inside(tuple(p[i] - d[i] for i in range(3))): continue
            line, q = [], p
            while inside(q): line.append(q); q = tuple(q[i] + d[i] for i in range(3))
            vs = [Q(*c) for c in line]
            if d in axis: cnf.append(vs)
            cnf += [[-a, -b] for a, b in itertools.combinations(vs, 2)]
    return cnf, Q
def add_nonclean(N, cnf, Q, first_free):
    """Satisfiable only if some neighbouring pair of columns differs in height by something other than
    the reference step (x-step from (0,0)->(1,0), y-step from (0,0)->(0,1)): i.e. the heights are NOT
    height = a*x + b*y + k mod N."""
    nxt = [first_free]
    def new():
        nxt[0] += 1; return nxt[0] - 1
    def diff_vars(c1, c2):
        D = [new() for _ in range(N)]
        for z in range(N):
            for dl in range(N):
                cnf.append([-Q(*c1, z), -Q(*c2, (z + dl) % N), D[dl]])
                cnf.append([-D[dl], -Q(*c1, z), Q(*c2, (z + dl) % N)])
        return D
    A = diff_vars((0, 0), (1, 0)); B = diff_vars((0, 0), (0, 1))
    wit = []
    for x in range(N):
        for y in range(N):
            for c2, R in (((x + 1, y), A), ((x, y + 1), B)):
                if c2[0] >= N or c2[1] >= N or ((x, y) == (0, 0) and c2 in ((1, 0), (0, 1))): continue
                D = diff_vars((x, y), c2)
                for dl in range(N):
                    w = new(); wit.append(w); cnf.append([-w, D[dl]]); cnf.append([-w, -R[dl]])
    cnf.append(wit)
