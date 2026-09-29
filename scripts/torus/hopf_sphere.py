"""Doughnut solutions on a sphere: the Hopf map with shifts folded away.

On the doughnut board, shifting a solution (r, c) -> (r + dr, c + dc) gives another solution. A shift
leaves the size of every Fourier component F(u, v) unchanged and turns its phase by an angle that
depends on the frequency. Call a solution together with all its shifts a "kind".

The Hopf map sends a pair of complex numbers (z1, z2), scaled to length 1, to a point on a sphere,
forgetting their shared phase:  (z1, z2) -> (2 Re z1 conj z2, 2 Im z1 conj z2, |z1|^2 - |z2|^2).

  plain    z1 = F(w1), z2 = F(w2) for two frequencies. A shift turns them by different angles, so
           only some shifts are folded away.
  paired   z1 = F(w)^2 / n, z2 = F(2w). Every shift turns both by the same angle, so all shifts are
           folded away and each kind lands on one point. (z1 conj z2 is F(w)^2 conj F(2w), known in
           signal processing as the bispectrum.)

For n = 13 this reports how the kinds spread under the plain map, that the paired map puts each kind
on one point, how well kinds are separated (with one and with several frequencies w), and whether
kinds related by a turn, mirror or scaling of the board share a point.

    python3 hopf_sphere.py             # seconds

Writes hopf_sphere.json for hopf_sphere.html. To view it locally, run `python3 -m http.server` in this
folder and open hopf_sphere.html.
"""
import json, itertools, collections
import numpy as np

n = 13
PAIRS = [(1, 2), (1, 3), (1, 4), (1, 5), (2, 3)]       # frequencies w for the paired map
PLAIN = ((1, 2), (1, 3))                               # frequencies w1, w2 for the plain map

def doughnut(n):
    out, s = [], [0] * n
    def go(r, cols, d1, d2):
        if r == n:
            out.append(s[:]); return
        for c in range(n):
            if c in cols or (r + c) % n in d1 or (r - c) % n in d2:
                continue
            s[r] = c
            go(r + 1, cols | {c}, d1 | {(r + c) % n}, d2 | {(r - c) % n})
    go(0, frozenset(), frozenset(), frozenset())
    return np.array(out)

def shift(s, dr, dc):
    t = np.empty(n, int)
    t[(np.arange(n) + dr) % n] = (s + dc) % n
    return t

def transform(s, M):
    """Apply a linear map M (mod n) to the queens of s."""
    t = np.empty(n, int)
    for r in range(n):
        c = s[r]
        t[(M[0][0] * r + M[0][1] * c) % n] = (M[1][0] * r + M[1][1] * c) % n
    return t

def hopf(z1, z2):
    norm = np.sqrt(abs(z1) ** 2 + abs(z2) ** 2)
    ok = norm > 1e-9
    a, b = z1 / np.where(ok, norm, 1), z2 / np.where(ok, norm, 1)
    ab = a * b.conj()
    return np.stack([2 * ab.real, 2 * ab.imag, abs(a) ** 2 - abs(b) ** 2], axis=1), ok

S = doughnut(n)
Q = len(S)
index = {tuple(s): i for i, s in enumerate(S)}
step = [int((s[1] - s[0]) % n) if len({(s[r] - s[0] - r * (s[1] - s[0])) % n for r in range(n)}) == 1 else None for s in S]
clean = np.array([a is not None for a in step])

kind = -np.ones(Q, int)
K = 0
for i in range(Q):
    if kind[i] < 0:
        for dr in range(n):
            for dc in range(n):
                kind[index[tuple(shift(S[i], dr, dc))]] = K
        K += 1
rep = [int(np.flatnonzero(kind == k)[0]) for k in range(K)]
print(f"{n} x {n} doughnut board: {Q} solutions ({clean.sum()} clean), {K} kinds "
      f"({len(set(kind[clean]))} clean, {len(set(kind[~clean]))} not clean)")

# families: kinds related by a turn, mirror or scaling (r, c) -> (m r, m c)
D4 = [((1, 0), (0, 1)), ((0, 1), (-1, 0)), ((-1, 0), (0, -1)), ((0, -1), (1, 0)),
      ((1, 0), (0, -1)), ((-1, 0), (0, 1)), ((0, 1), (1, 0)), ((0, -1), (-1, 0))]
maps = [((m * a[0], m * a[1]), (m * b[0], m * b[1])) for m in range(1, n) for a, b in D4]
family = -np.ones(K, int)
nf = 0
for k in range(K):
    if family[k] < 0:
        for M in maps:
            family[kind[index[tuple(transform(S[rep[k]], M))]]] = nf
        nf += 1
print(f"with turns, mirrors and scalings: {nf} families "
      f"({len(set(family[kind[clean]]))} clean, {len(set(family[kind[~clean]]))} not clean)")

F = np.array([np.fft.fft2(np.eye(n)[s]) for s in S])

# plain map: how many points does one kind cover?
p, ok = hopf(F[:, PLAIN[0][0], PLAIN[0][1]], F[:, PLAIN[1][0], PLAIN[1][1]])
plain_pts = {}
for k in range(K):
    m = (kind == k) & ok
    if m.any():
        plain_pts[k] = np.unique(np.round(p[m], 6), axis=0)
spread = collections.Counter(len(v) for v in plain_pts.values())
print(f"\nplain map, w1 = {PLAIN[0]}, w2 = {PLAIN[1]}: {len(plain_pts)} kinds shown; points per kind: {dict(sorted(spread.items()))}")

# paired map
paired = {}
for w in PAIRS:
    w2 = ((2 * w[0]) % n, (2 * w[1]) % n)
    p, ok = hopf(F[:, w[0], w[1]] ** 2 / n, F[:, w2[0], w2[1]])
    worst, pts = 0.0, {}
    for k in range(K):
        m = (kind == k) & ok
        if m.any():
            worst = max(worst, np.abs(p[m] - p[m][0]).max())
            pts[k] = p[m][0]
    paired[w] = pts
    same = collections.Counter(tuple(np.round(v, 6)) for v in pts.values())
    shared = sum(c for c in same.values() if c > 1)
    fam_pairs = [(a, b) for a, b in itertools.combinations(pts, 2) if family[a] == family[b]]
    fam_same = sum(np.abs(pts[a] - pts[b]).max() < 1e-6 for a, b in fam_pairs)
    print(f"paired map, w = {w}: {len(pts)} kinds shown ({sum(clean[rep[k]] for k in pts)} clean); "
          f"largest spread inside a kind {worst:.1e}; {len(same)} distinct points ({shared} kinds share one); "
          f"same-family pairs on one point: {fam_same} of {len(fam_pairs)}")

print()
for r in range(2, len(PAIRS) + 1):
    ws = PAIRS[:r]
    covered = set().union(*[set(paired[w]) for w in ws])
    keys = collections.Counter(tuple(np.round(np.concatenate([paired[w].get(k, np.full(3, 9.0)) for w in ws]), 5))
                               for k in covered)
    print(f"first {r} frequencies together: {len(covered)} of {K} kinds shown, all on different points: {max(keys.values()) == 1}")

out = {
    "n": n,
    "pairs": [list(w) for w in PAIRS],
    "plainPair": [list(w) for w in PLAIN],
    "kinds": [{
        "board": "".join(f"{c:x}" for c in S[rep[k]]),
        "size": int((kind == k).sum()),
        "clean": bool(clean[rep[k]]),
        "step": step[rep[k]],
        "family": int(family[k]),
        "paired": {f"{w[0]},{w[1]}": [round(float(x), 5) for x in paired[w][k]] for w in PAIRS if k in paired[w]},
        "plain": [[round(float(x), 5) for x in pt] for pt in plain_pts.get(k, [])],
    } for k in range(K)],
}
json.dump(out, open("hopf_sphere.json", "w"), separators=(",", ":"))
print("\nwrote hopf_sphere.json")
