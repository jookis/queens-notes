import itertools, random, sys, time
# Same bar search as observers.py, but every sightline (beam) has a weight. When a bar is stuck (its best
# height is no better than where it was), every beam still blocked at its new spot gets heavier by 1, so
# beams that stay blocked shout louder until the search clears them ("alive beams", driven by results).
def run(n, dirs, steps, seed, noise):
    rnd = random.Random(seed)
    inside = lambda p: all(0 <= c < n for c in p)
    line = {}
    for d in dirs:
        for p in itertools.product(range(n), repeat=3):
            q = p
            while inside(tuple(q[i] - d[i] for i in range(3))): q = tuple(q[i] - d[i] for i in range(3))
            line[d, p] = (d, q)
    h = {(x, y): rnd.randrange(n) for x in range(n) for y in range(n)}
    cnt, w = {}, {}
    def add(b, z, s):
        for d in dirs:
            k = line[d, (*b, z)]; cnt[k] = cnt.get(k, 0) + s
    for b, z in h.items(): add(b, z, 1)
    blocked = lambda b, z: any(cnt.get(line[d, (*b, z)], 0) > 1 for d in dirs)
    cost = lambda b, z: sum(w.get(line[d, (*b, z)], 1) * cnt.get(line[d, (*b, z)], 0) for d in dirs)
    for step in range(steps):
        bad = [b for b, z in h.items() if blocked(b, z)]
        if not bad: return step
        b = rnd.choice(bad); add(b, h[b], -1); old = cost(b, h[b])
        if rnd.random() < noise: z = rnd.randrange(n)
        else:
            c = [cost(b, z) for z in range(n)]; m = min(c)
            z = rnd.choice([z for z in range(n) if c[z] == m])
        stuck = cost(b, z) >= old
        h[b] = z; add(b, z, 1)
        if stuck:
            for d in dirs:
                k = line[d, (*b, z)]
                if cnt[k] > 1: w[k] = w.get(k, 1) + 1
    return None
sides, corners = [(1, 0, 0), (0, 1, 0)], [(1, 1, 0), (1, -1, 0)]
tilted = [(1, 0, 1), (1, 0, -1), (0, 1, 1), (0, 1, -1), (1, 1, 1), (1, 1, -1), (1, -1, 1), (1, -1, -1)]
n, which, steps, seeds, noise = int(sys.argv[1]), sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), float(sys.argv[5])
dirs = sides + corners if which == "horizontal" else sides + corners + tilted
t = time.time(); res = [run(n, dirs, steps, 100 + s, noise) for s in range(seeds)]
ok = sorted(r for r in res if r is not None)
print(f"{n}: {which:10} alive beams, noise {noise}: solved {len(ok)}/{seeds} within {steps} steps, steps used {ok}  ({time.time() - t:.0f} s)")
