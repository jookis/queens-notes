import itertools, random, sys, time
# Board of bars: bar (x, y) has height h, the queen sits on top at (x, y, h). An observer looks along one
# direction and sees one sightline per line of the cube; the rule is "no sightline sees two queens".
def run(n, dirs, steps, seed, noise=0.1):
    rnd = random.Random(seed)
    inside = lambda p: all(0 <= c < n for c in p)
    line = {}                                         # (direction, cell) -> sightline id
    for d in dirs:
        for p in itertools.product(range(n), repeat=3):
            q = p
            while inside(tuple(q[i] - d[i] for i in range(3))): q = tuple(q[i] - d[i] for i in range(3))
            line[d, p] = (d, q)
    h = {(x, y): rnd.randrange(n) for x in range(n) for y in range(n)}
    cnt = {}
    def add(b, z, s):
        for d in dirs:
            k = line[d, (*b, z)]; cnt[k] = cnt.get(k, 0) + s
    for b, z in h.items(): add(b, z, 1)
    seen = lambda b, z: sum(cnt.get(line[d, (*b, z)], 0) for d in dirs)
    for step in range(steps):
        bad = [b for b, z in h.items() if seen(b, z) > len(dirs)]       # its own count is 1 per observer
        if not bad: return step, h
        b = rnd.choice(bad); add(b, h[b], -1)
        if rnd.random() < noise: z = rnd.randrange(n)
        else:
            cost = [seen(b, z) for z in range(n)]; m = min(cost)
            z = rnd.choice([z for z in range(n) if cost[z] == m])
        h[b] = z; add(b, z, 1)
    return None, h
sides, corners = [(1, 0, 0), (0, 1, 0)], [(1, 1, 0), (1, -1, 0)]
tilted = [(1, 0, 1), (1, 0, -1), (0, 1, 1), (0, 1, -1), (1, 1, 1), (1, 1, -1), (1, -1, 1), (1, -1, -1)]
for n in (11, 13):
    for name, dirs, steps in (("2 sides + 2 corners (horizontal)", sides + corners, 20000),
                              ("all 12 observers (full cube)", sides + corners + tilted, int(sys.argv[1]))):
        t = time.time(); res = [run(n, dirs, steps, s)[0] for s in range(5)]
        ok = [r for r in res if r is not None]
        print(f"{n}: {name:34} solved {len(ok)}/5 runs, steps {ok if ok else '-'}  (limit {steps}, {time.time() - t:.0f} s)", flush=True)
