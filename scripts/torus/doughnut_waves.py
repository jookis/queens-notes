import numpy as np, collections
def doughnut(n):
    sols = []
    def go(r, cols, d1, d2, path):
        if r == n: sols.append(tuple(path)); return
        for c in range(n):
            if c not in cols and (r + c) % n not in d1 and (r - c) % n not in d2:
                go(r + 1, cols | {c}, d1 | {(r + c) % n}, d2 | {(r - c) % n}, path + [c])
    go(0, frozenset(), frozenset(), frozenset(), []); return sols
for n in (11, 13):
    sols = doughnut(n)
    lin = [s for s in sols if len({(s[r] - s[0] - r * (s[1] - s[0])) % n for r in range(n)}) == 1]
    quiet = [(t, 0) for t in range(1, n)] + [(0, t) for t in range(1, n)] + [(t, t) for t in range(1, n)] + [(t, -t % n) for t in range(1, n)]
    worst_quiet, loud = 0.0, collections.Counter()
    for s in sols:
        f = np.zeros((n, n)); f[list(range(n)), list(s)] = 1
        F = np.abs(np.fft.fft2(f))
        worst_quiet = max(worst_quiet, max(F[q] for q in quiet))
        loud[int((F > 1e-6).sum()) - 1] += 1          # sounding frequencies, not counting the centre
    print(f"{n}x{n} doughnut solutions: {len(sols)}, single-step (clean) {len(lin)}, messy {len(sols) - len(lin)}")
    print(f"   loudest value on the 4 quiet lines, over all solutions: {worst_quiet:.1e}  (queens rule says 0)")
    print(f"   sounding frequencies per solution (count: solutions): {dict(sorted(loud.items()))}")
