"""Do the 4 learned classes of aligned_heat.py come back at other board sizes?

Fits the 4 classes three times (three random starts) for n = 10 to 13, and once more for random rook
placements at n = 12 (one per row and column, diagonals ignored) as a baseline. Every class map is
turned into log(count / average), then resampled to a 24 x 24 grid on the unit square so that maps of
different sizes can be compared.

Two fits are compared by matching their classes one to one and averaging the correlations of the
matched maps (1 = identical). Two versions:
  turn    each class may take its own turn or mirror
  shift   each class may also shift by up to a quarter of the board, to test whether a pattern comes
          back "in another place"

Freedom to turn and shift makes any two maps look more alike, so compare against the baselines:
two fits at the same n, and queen classes against random-rook classes.

    python3 classes_across_n.py        # about 10 minutes, mostly fitting n = 13
"""
import itertools, time
import numpy as np

# aligned_heat.py runs its whole study when imported, so take only its functions (everything above
# its "run" marker).
exec(open("aligned_heat.py").read().split("# ---------- run ----------")[0])

G, SH = 24, 6          # common grid on the unit square; shifts up to a quarter of it

def resample(M):
    n = M.shape[0]
    x = (np.arange(n) + 0.5) / n
    t = (np.arange(G) + 0.5) / G
    A = np.array([np.interp(t, x, row) for row in M])
    return np.array([np.interp(t, x, col) for col in A.T]).T

def turns(M):
    out, t = [], M
    for _ in range(4):
        out += [t, t[:, ::-1]]
        t = np.rot90(t)
    return out

def class_maps(C):
    return [resample(np.log((C[c] + PSEUDO) / (C[c] + PSEUDO).mean())) for c in range(C.shape[0])]

def corr(a, b):
    a = a - a.mean(); b = b - b.mean()
    return (a * b).sum() / np.sqrt((a * a).sum() * (b * b).sum())

def pair_score(a, b, mode):
    best = -1
    for bt in turns(b):
        if mode == "turn":
            best = max(best, corr(a, bt))
            continue
        for dx in range(-SH, SH + 1):
            for dy in range(-SH, SH + 1):
                A = a[max(dx, 0):G + min(dx, 0), max(dy, 0):G + min(dy, 0)]
                B = bt[max(-dx, 0):G + min(-dx, 0), max(-dy, 0):G + min(-dy, 0)]
                best = max(best, corr(A, B))
    return best

def similarity(A, B, mode):
    """Each class may take its own turn (and shift); classes matched one to one for the best mean."""
    M = np.array([[pair_score(a, b, mode) for b in B] for a in A])
    return max(M[np.arange(K), p].mean() for p in itertools.permutations(range(K)))

fits = {}
for n in (10, 11, 12, 13):
    t0 = time.time()
    P = poses(solutions(n))
    fits[n] = [class_maps(best_fit(P, K, seed=s)[0][3]) for s in (100 + n, 7, 8)]
    print(f"fitted n = {n} ({time.time() - t0:.0f} s)", flush=True)
rng = np.random.default_rng(12)
R = poses(np.array([rng.permutation(12) for _ in range(14200)]))
fits["rooks12"] = [class_maps(best_fit(R, K, seed=s)[0][3]) for s in (112, 7, 8)]
print("fitted random rooks, n = 12", flush=True)

for mode, label in (("turn", "each class its own turn"),
                    ("shift", "each class its own turn and shift (up to 1/4 board)")):
    print(f"\n{label}:")
    for n in (10, 11, 12, 13):
        within = [similarity(fits[n][i], fits[n][j], mode) for i, j in ((0, 1), (0, 2), (1, 2))]
        line = f"  n = {n}: same n, other start {np.mean(within):.2f}"
        if n + 1 in fits:
            across = [similarity(fits[n][i], fits[n + 1][j], mode) for i in range(3) for j in range(3)]
            line += f"   | n vs n+1 {np.mean(across):.2f} ({min(across):.2f}-{max(across):.2f})"
        if n in (12, 13):
            rk = [similarity(fits[n][i], fits["rooks12"][j], mode) for i in range(3) for j in range(3)]
            line += f"   | vs random-rook classes {np.mean(rk):.2f} ({min(rk):.2f}-{max(rk):.2f})"
        print(line, flush=True)
    rr = [similarity(fits["rooks12"][i], fits["rooks12"][j], mode) for i, j in ((0, 1), (0, 2), (1, 2))]
    print(f"  random rooks n = 12, other start: {np.mean(rr):.2f}", flush=True)
