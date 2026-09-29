"""Aligned and per-family density maps: turn each solution before stacking, or stack families apart.

The plain map (queens_heat.rs) stacks all 8 turns and mirrors of every solution, so it is forced to be
8-way symmetric and different kinds of solution blur together. Here:

  aligned   each solution is turned into the pose that best matches the current average, then the
            average is recomputed, until nothing changes (the cryo-EM "align, then average" loop).
  symmetry  exact families by how much symmetry a solution has: none, half-turn, quarter-turn.
  classes   k maps learned together: each solution picks the (map, pose) pair that fits it best.

Aligning always sharpens a map, even for random data, because the poses are picked to fit. So every
number is also computed for random rook placements (one per row and column, diagonals ignored) with
the same count, and the maps are scored on solutions that were not used to build them.

A map is scored as a row-by-row model p(column | row). The score is how many bits per queen it saves
against guessing uniformly, measured on held-out families (whole symmetry orbits, so no test
solution is a turned copy of a training one). For the aligned and class models the pose
and class are summed over (a mixture), so they get no free bits from choosing.

    python3 aligned_heat.py            # n = 8 to 12
    python3 aligned_heat.py 8 10       # a smaller range

Writes aligned_heat.png: one row of small maps per n, in this order:
  plain | aligned | no symmetry | half-turn | quarter-turn (blank if none) | class 1 .. class 4 |
  random rooks aligned the same way (what alignment makes out of pure noise)
Each map is scaled on its own, light = few queens, dark = many.
"""
import sys, zlib, struct
import numpy as np

K = 4            # number of learned classes
SEEDS = 8        # restarts per fit, the best one is kept
PSEUDO = 0.5     # pseudo-count per square, so unseen squares are not impossible

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
    """All 8 turns and mirrors of every solution: shape (Q, 8, n), entry [q, g, row] = column."""
    Q, n = S.shape
    rows = np.arange(n)
    out, t = [], S
    for _ in range(4):
        out += [t, n - 1 - t]                                  # as is, and mirrored left-right
        u = np.empty_like(t); u[np.arange(Q)[:, None], t] = n - 1 - rows   # quarter turn
        t = u
    return np.stack(out, axis=1)

def counts(P, pose, cls, k, n):
    """Queen counts per class from the chosen pose of each solution: shape (k, n, n)."""
    C = np.zeros((k, n, n))
    chosen = P[np.arange(len(P)), pose]                        # (Q, n)
    for r in range(n):
        np.add.at(C, (cls, r, chosen[:, r]), 1)
    return C

def logp(C):
    """Row-wise log probabilities from counts, with a pseudo-count: log p(column | row, class)."""
    C = C + PSEUDO
    return np.log(C / C.sum(axis=2, keepdims=True))

def score_all(P, L, weights):
    """log p(pose g of solution q | class c) for every q, class, pose: shape (Q, k, 8)."""
    n = P.shape[2]
    rows = np.arange(n)
    return L[:, rows, P].sum(axis=-1).transpose(1, 0, 2) + np.log(weights)[None, :, None]

def fit(P, k, rng, iters=60):
    """Hard alignment and classification: repeat (pick best class and pose, rebuild the maps)."""
    Q, _, n = P.shape
    pose = rng.integers(8, size=Q)
    cls = rng.integers(k, size=Q)
    for _ in range(iters):
        C = counts(P, pose, cls, k, n)
        w = (np.bincount(cls, minlength=k) + 1) / (Q + k)
        s = score_all(P, logp(C), w).reshape(Q, -1)
        best = s.argmax(axis=1)
        new_cls, new_pose = best // 8, best % 8
        if np.array_equal(new_cls, cls) and np.array_equal(new_pose, pose):
            break
        cls, pose = new_cls, new_pose
    total = s.max(axis=1).sum()
    return total, cls, pose, counts(P, pose, cls, k, n), w

def best_fit(P, k, seed):
    rng = np.random.default_rng(seed)
    runs = [fit(P, k, rng) for _ in range(SEEDS)]
    return max(runs, key=lambda r: r[0]), runs

def heldout_bits(P_train, P_test, k, aligned, seed):
    """Bits per queen saved on the test half by a model built on the train half."""
    n = P_train.shape[2]
    if aligned:
        (_, _, _, C, w), _ = best_fit(P_train, k, seed)
        s = score_all(P_test, logp(C), w)                      # (Q, k, 8)
        m = s.max(axis=(1, 2), keepdims=True)
        ll = (m.squeeze() + np.log(np.exp(s - m).sum(axis=(1, 2)) / 8))
    else:                                                      # plain map: all poses stacked
        Q = len(P_train)
        C = counts(P_train.reshape(-1, 1, n), np.zeros(Q * 8, int), np.zeros(Q * 8, int), 1, n)
        ll = score_all(P_test[:, :1], logp(C), np.ones(1)).ravel()
    return (np.log2(n) * n + ll.mean() / np.log(2)) / n

def rand_index_adj(a, b):
    """Adjusted Rand index: 1 = same split, about 0 = no more alike than chance."""
    T = np.zeros((a.max() + 1, b.max() + 1))
    np.add.at(T, (a, b), 1)
    c2 = lambda x: (x * (x - 1) / 2).sum()
    s, sa, sb, tot = c2(T), c2(T.sum(1)), c2(T.sum(0)), c2(np.array([T.sum()]))
    e = sa * sb / tot
    return (s - e) / ((sa + sb) / 2 - e)

def representatives(P):
    """One solution per family (orbit under the 8 turns and mirrors), as its smallest pose."""
    Q, _, n = P.shape
    key = (P * n ** np.arange(n - 1, -1, -1)).sum(axis=2)     # read each pose as a number
    return np.unique(P[np.arange(Q), key.argmin(axis=1)], axis=0)

def symmetry_type(P):
    """0 = no symmetry, 1 = same after half turn only, 2 = same after quarter turn."""
    same = (P == P[:, :1]).all(axis=2)                         # (Q, 8): which poses equal the original
    quarter = same[:, 2]
    half = same[:, 4]
    return np.where(quarter, 2, np.where(half, 1, 0))

def contrast(M):
    d = M / M.mean()
    return d.std()

def rooks(n, Q, rng):
    return np.array([rng.permutation(n) for _ in range(Q)])

# ---------- picture ----------
RAMP = ["#cde2fb", "#b7d3f6", "#9ec5f4", "#86b6ef", "#6da7ec", "#5598e7", "#3987e5",
        "#2a78d6", "#256abf", "#1c5cab", "#184f95", "#104281", "#0d366b"]
RAMP = np.array([[int(h[i:i + 2], 16) for i in (1, 3, 5)] for h in RAMP], float)

def tile(M, px=120):
    n = M.shape[0]
    img = np.full((px, px, 3), 255, np.uint8)
    if M.sum() == 0:
        return img
    lo, hi = M.min(), M.max()
    t = (M - lo) / (hi - lo) if hi > lo else np.zeros_like(M)
    x = t * (len(RAMP) - 1)
    i = np.clip(np.floor(x).astype(int), 0, len(RAMP) - 2)
    f = (x - i)[..., None]
    col = RAMP[i] * (1 - f) + RAMP[i + 1] * f
    cell = px // n
    off = (px - cell * n) // 2
    for r in range(n):
        for c in range(n):
            img[off + r * cell: off + (r + 1) * cell - 1, off + c * cell: off + (c + 1) * cell - 1] = col[r, c]
    return img

def png(a, fn):
    h, w = a.shape[:2]
    raw = b''.join(b'\x00' + a[i].tobytes() for i in range(h))
    ch = lambda tg, d: struct.pack('>I', len(d)) + tg + d + struct.pack('>I', zlib.crc32(tg + d) & 0xffffffff)
    open(fn, 'wb').write(b'\x89PNG\r\n\x1a\n' + ch(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0))
                         + ch(b'IDAT', zlib.compress(raw, 9)) + ch(b'IEND', b''))

# ---------- run ----------
lo, hi = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) > 2 else (8, 12)
gap = np.full((120, 8, 3), 255, np.uint8)
picture = []

print(" n       Q   contrast: plain  aligned  (rooks aligned)")
report = []
for n in range(lo, hi + 1):
    S = solutions(n)
    Q = len(S)
    P = poses(S)
    rng = np.random.default_rng(n)
    R = poses(rooks(n, Q, rng))

    plain = counts(P.reshape(-1, 1, n), np.zeros(Q * 8, int), np.zeros(Q * 8, int), 1, n)[0]
    (_, _, pose1, C1, _), _ = best_fit(P, 1, seed=n)
    (_, _, _, R1, _), _ = best_fit(R, 1, seed=n)
    print(f"{n:2d} {Q:7d}          {contrast(plain):6.3f}   {contrast(C1[0]):6.3f}   ({contrast(R1[0]):6.3f})")

    sym = symmetry_type(P)
    fam = [counts(P[sym == t], pose1[sym == t], np.zeros((sym == t).sum(), int), 1, n)[0] for t in (0, 1, 2)]

    (_, clsK, poseK, CK, _), runs = best_fit(P, K, seed=100 + n)
    order = np.argsort(-np.bincount(clsK, minlength=K))
    agree = np.mean([rand_index_adj(clsK, r[1]) for r in runs])
    (_, clsR, _, _, _), runsR = best_fit(R, K, seed=100 + n)
    agreeR = np.mean([rand_index_adj(clsR, r[1]) for r in runsR])

    # held-out halves are split by family, so no test solution is a turned copy of a training one
    F = poses(representatives(P))
    FR = poses(rooks(n, len(F), rng))
    bits, bitsR = [], []
    for X, out in ((F, bits), (FR, bitsR)):
        h = rng.permutation(len(X))
        tr, te = X[h[: len(X) // 2]], X[h[len(X) // 2:]]
        out += [heldout_bits(tr, te, 1, False, n), heldout_bits(tr, te, 1, True, n),
                heldout_bits(tr, te, K, True, n)]
    report.append((n, len(F), np.bincount(sym, minlength=3), np.bincount(clsK, minlength=K)[order],
                   agree, agreeR, bits, bitsR))

    row = [tile(plain), tile(C1[0])] + [tile(f) for f in fam] + [tile(CK[c]) for c in order] + [tile(R1[0])]
    picture.append(np.hstack([x for t in row for x in (t, gap)]))
    picture.append(np.full((8, picture[-1].shape[1], 3), 255, np.uint8))

print("\n n   families by symmetry     class sizes            class split repeats  (rooks)")
print("     none  half  quarter")
for n, _, fs, cs, a, aR, _, _ in report:
    print(f"{n:2d}  {fs[0]:5d} {fs[1]:5d} {fs[2]:6d}     {' '.join(f'{c:5d}' for c in cs)}      {a:6.2f}            ({aR:5.2f})")

print("\nBits per queen saved on held-out families (higher = the map predicts better):")
print(" n  families   plain   aligned   4 classes  |  rooks: plain  aligned  4 classes")
for n, nf, *_, b, bR in report:
    print(f"{n:2d}  {nf:6d}   {b[0]:6.3f}   {b[1]:6.3f}    {b[2]:6.3f}    |       {bR[0]:6.3f}   {bR[1]:6.3f}    {bR[2]:6.3f}")

png(np.ascontiguousarray(np.vstack(picture)), 'aligned_heat.png')
print("\nwrote aligned_heat.png")
