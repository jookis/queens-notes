"""One dot per solution: lay out all solution families in the plane, so similar ones sit close together.

Each family (a solution with all its turns and mirrors) becomes one dot. The distance between two
families is how many queens differ after the best turn or mirror:

    d(s, t) = n - max over the 8 poses g of #{rows r : g(s)[r] = t[r]}

The dots are placed by classical multidimensional scaling (MDS): the two directions that keep as much
of these distances as possible. MDS does not invent clusters (unlike t-SNE or UMAP), so if groups show
up they are in the distances.

Pictures of a cloud are hard to judge by eye, so the same is done for random rook placements (one per
row and column, diagonals ignored) with the same number of families, and three numbers are compared:

  top-2 share   how much of the spread the two plotted directions hold. Small = the plane view hides
                most of the structure.
  nearest       the average distance to the closest other family. Clusters make this small.
  bimodality    Sarle's coefficient on each of the first two axes: above 0.555 hints at two groups.
  web           link two families when they differ in at most k queens, and count the linked groups.

For n = 11 the linear solutions (column = a*row + b mod n) are marked, to see whether they sit apart.

    python3 solution_plane.py          # n = 8 to 12, about a minute
    python3 solution_plane.py 8 10

Writes solution_plane.json (dots, boards, two-queen links and numbers) for solution_plane.html. To view
it locally, run `python3 -m http.server` in this folder and open solution_plane.html.
"""
import sys, json
import numpy as np

def solutions(n):
    out, s, full = [], [0] * n, (1 << n) - 1
    def go(r, cols, d1, d2):
        if r == n:
            out.append(s[:]); return
        free = full & ~(cols | d1 | d2)
        while free:
            b = free & -free; free ^= b
            s[r] = b.bit_length() - 1
            go(r + 1, cols | b, ((d1 | b) << 1) & full, (d2 | b) >> 1)
    go(0, 0, 0, 0)
    return np.array(out, dtype=np.int64)

def poses(S):
    """All 8 turns and mirrors: shape (Q, 8, n), entry [q, g, row] = column."""
    Q, n = S.shape
    rows = np.arange(n)
    out, t = [], S
    for _ in range(4):
        out += [t, n - 1 - t]
        u = np.empty_like(t); u[np.arange(Q)[:, None], t] = n - 1 - rows
        t = u
    return np.stack(out, axis=1)

def representatives(S):
    """One board per family, as its smallest pose (read as a number)."""
    P = poses(S)
    n = S.shape[1]
    key = (P * n ** np.arange(n - 1, -1, -1)).sum(axis=2)
    return np.unique(P[np.arange(len(S)), key.argmin(axis=1)], axis=0)

def symmetry_type(F):
    """0 = none, 1 = same after half turn only, 2 = same after quarter turn."""
    same = (poses(F) == F[:, None, :]).all(axis=2)
    return np.where(same[:, 2], 2, np.where(same[:, 4], 1, 0))

def distances(F, chunk=64):
    P = poses(F)
    m, n = F.shape
    D = np.empty((m, m), np.int64)
    for i in range(0, m, chunk):
        shared = (P[i:i + chunk, :, None, :] == F[None, None, :, :]).sum(axis=3)   # (c, 8, m)
        D[i:i + chunk] = n - shared.max(axis=1)
    return D

def mds(D):
    m = len(D)
    J = np.eye(m) - 1 / m
    B = -0.5 * J @ (D.astype(float) ** 2) @ J
    w, v = np.linalg.eigh(B)
    w, v = w[::-1], v[:, ::-1]
    xy = v[:, :2] * np.sqrt(np.maximum(w[:2], 0))
    return xy, w[:2].sum() / w[w > 0].sum()

def bimodality(x):
    """Sarle's bimodality coefficient; 0.555 is the value for a flat (uniform) spread."""
    m = len(x)
    z = (x - x.mean()) / x.std()
    g, k = (z ** 3).mean(), (z ** 4).mean() - 3
    return (g * g + 1) / (k + 3 * (m - 1) ** 2 / ((m - 2) * (m - 3)))

def linear(F):
    """Families that contain a board with column = a*row + b mod n."""
    n = F.shape[1]
    P = poses(F)
    d = (P[:, :, 1:] - P[:, :, :-1]) % n
    return (d == d[:, :, :1]).all(axis=2).any(axis=1)

def groups(D, k):
    """Sizes of the groups formed by linking families at distance <= k."""
    m = len(D); lab = -np.ones(m, int); c = 0
    for i in range(m):
        if lab[i] >= 0: continue
        stack = [i]; lab[i] = c
        while stack:
            j = stack.pop()
            for t in np.nonzero((D[j] <= k) & (lab < 0))[0]:
                lab[t] = c; stack.append(t)
        c += 1
    return np.bincount(lab)

def web(D):
    near = np.where(np.eye(len(D), dtype=bool), D.max() + 1, D).min(axis=1)
    g3, g4 = groups(D, 3), groups(D, 4)
    web.last = {"near2": int((near == 2).sum()), "largest4": int(g4.max()), "alone4": int((g4 == 1).sum())}
    return (f"nearest at 2 / 3 / 4+ queens: {(near == 2).sum():4d} {(near == 3).sum():4d} {(near >= 4).sum():4d}"
            f"   linked at <=4: largest group {g4.max():4d}, alone {(g4 == 1).sum():4d}"
            f"   (at <=3: largest {g3.max()})")

def summary(F):
    D = distances(F)
    xy, share = mds(D)
    near = np.where(np.eye(len(D), dtype=bool), D.max() + 1, D).min(axis=1)
    return D, xy, share, near.mean(), [bimodality(xy[:, 0]), bimodality(xy[:, 1])]

lo, hi = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) > 2 else (8, 12)
out, webs = {}, []
print(" n  families   top-2 share      nearest       bimodality (axis 1, 2)")
print("               queens rooks   queens rooks    queens         rooks")
for n in range(lo, hi + 1):
    F = representatives(solutions(n))
    rng = np.random.default_rng(n)
    R = representatives(np.array([rng.permutation(n) for _ in range(len(F))]))
    D, xy, share, near, bim = summary(F)
    DR, xyR, shareR, nearR, bimR = summary(R)
    print(f"{n:2d}  {len(F):7d}    {share:5.3f}  {shareR:5.3f}    {near:5.2f}  {nearR:5.2f}   "
          f"{bim[0]:.2f} {bim[1]:.2f}      {bimR[0]:.2f} {bimR[1]:.2f}")
    wq = web(D); webQ = web.last
    wr = web(DR); webR = web.last
    webs.append((n, wq, wr))
    sym, lin = symmetry_type(F), linear(F)
    if lin.any():
        rest = ~lin
        centre = np.linalg.norm(xy - xy.mean(axis=0), axis=1)
        print(f"      {lin.sum()} linear families: mean distance to the others {D[lin][:, rest].mean():.2f} "
              f"(others among themselves {D[rest][:, rest].mean():.2f}); "
              f"distance from the centre of the plane {centre[lin].mean():.2f} vs {centre[rest].mean():.2f}")
    out[n] = {"families": len(F), "share": share, "shareRooks": shareR, "nearest": near,
              "nearestRooks": nearR, "bimodality": bim, "bimodalityRooks": bimR,
              "dots": [[round(float(a), 3), round(float(b), 3), int(t), bool(l), "".join(f"{c:x}" for c in f)]
                       for (a, b), t, l, f in zip(xy, sym, lin, F)],
              "web": webQ, "webRooks": webR,
              "twins": [[int(i), int(j)] for i, j in zip(*np.nonzero(np.triu(D == 2)))],
              "rooks": [[round(float(a), 3), round(float(b), 3)] for a, b in xyR]}

print("\nThe web of small moves (families = dots):")
for n, q, r in webs:
    print(f"{n:2d} queens  {q}\n   rooks   {r}")

json.dump(out, open("solution_plane.json", "w"), separators=(",", ":"))
print("\nwrote solution_plane.json")
