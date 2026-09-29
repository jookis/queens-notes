"""Flat-board solutions on a sphere: every solution its own point, placed by two of its waves.

Take the 2-D Fourier transform of a board (1 on queens), measured from the centre of the board:
F(u, v) = sum over rows r of exp(-2 pi i (u (r - m) + v (s[r] - m)) / n) with m = (n - 1) / 2. (Measured
from the corner square instead, every longitude turns by a fixed angle, 30 degrees at n = 12, and the
picture is harder to read.) The Hopf map sends two waves (z1, z2), scaled to length 1, to the point
(2 Re z1 conj z2, 2 Im z1 conj z2, |z1|^2 - |z2|^2) on a sphere: top = only z1 sounds, bottom = only z2,
and the longitude is their phase difference. The flat board has no shifts, so nothing is folded away
here; the sphere is just a place where each solution gets a spot.

Two choices of waves:
  diagonal  z1 = F(1, 1), z2 = F(1, -1): the diagonal and the anti-diagonal wave, mirror images of
            each other. Easy to read. (With the centre as origin, F(1, n - 1) is not the same wave on an
            even board: it differs by a sign, which turns every longitude by 180 degrees.)
  spread    the pair of waves (out of all pairs of non-axis frequencies) that gives the most distinct
            points, so that as few solutions as possible share a spot.

Solutions where both waves are silent get no point (at n = 11 the 88 doughnut solutions, for the
diagonal pair). For each choice, compared with the same number of random rook placements (one per row
and column, diagonals ignored): how many distinct points, the largest number of solutions on one point,
and how many of the 8 turns and mirrors of a solution land on different points.

For the diagonal pair also:
  mirrors   how flipping the board top to bottom, turning it half way, and mirroring it left to right
            move a spot (checked exactly for every solution)
  phase     how strongly the longitudes lean towards 0 (the two waves in step, seen from the centre)
  rows      how many latitude levels and loudness values of the diagonal wave occur

    python3 flat_sphere.py             # n = 10 to 12, about two minutes (the pair search)
    python3 flat_sphere.py 10 11

Writes flat_sphere.json for flat_sphere.html. To view it locally, run `python3 -m http.server` in this
folder and open flat_sphere.html.
"""
import sys, json, collections
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

def wave(S, u, v):
    n = S.shape[1]
    m = (n - 1) / 2
    return np.exp(-2j * np.pi * (u * (np.arange(n)[None, :] - m) + v * (S - m)) / n).sum(axis=1)

def hopf(z1, z2):
    norm = np.sqrt(abs(z1) ** 2 + abs(z2) ** 2)
    ok = norm > 1e-9
    a, b = z1 / np.where(ok, norm, 1), z2 / np.where(ok, norm, 1)
    ab = a * b.conj()
    return np.stack([2 * ab.real, 2 * ab.imag, abs(a) ** 2 - abs(b) ** 2], axis=1), ok

def stacks(P):
    """For each point, how many points share it (to 5 decimals)."""
    keys = [tuple(k) for k in np.round(P, 5)]
    c = collections.Counter(keys)
    return np.array([c[k] for k in keys]), len(c)

def images(s):
    n = len(s); out, t = [], tuple(s)
    for _ in range(4):
        out += [t, tuple(reversed(t))]
        u = [0] * n
        for r, c in enumerate(t):
            u[c] = n - 1 - r
        t = tuple(u)
    return out

def diagonal_extras(S, R, P, PR, ok, okR, index, z1):
    n = S.shape[1]
    h, lon = P[:, 2], np.arctan2(P[:, 1], P[:, 0])
    good = ok & (abs(h) < 0.999)                       # longitude is meaningless at the poles
    def check(name, g):
        j = np.array([index[tuple(g(s))] for s in S])
        height = "height kept" if np.allclose(h[j][ok], h[ok]) else \
                 "top and bottom swap" if np.allclose(h[j][ok], -h[ok]) else "height changes"
        m = good & good[j]
        rule = next((w for sg, w in ((1, "longitude kept"), (-1, "longitude reversed"))
                     if np.allclose(np.angle(np.exp(1j * (lon[j][m] - sg * lon[m]))), 0, atol=1e-6)), "longitude: no fixed rule")
        print(f"      {name}: {height}, {rule}")
    print("   diagonal waves, how the board's symmetries move a spot:")
    check("flip top to bottom", lambda s: s[::-1])
    check("half turn", lambda s: (len(s) - 1 - s)[::-1])
    check("mirror left to right", lambda s: len(s) - 1 - s)
    lean = np.exp(1j * lon[good]).mean()
    leanR = np.exp(1j * np.arctan2(PR[okR, 1], PR[okR, 0])).mean()
    near = (abs(lon[good]) < np.pi / 6).mean()
    nearR = (abs(np.arctan2(PR[okR, 1], PR[okR, 0])) < np.pi / 6).mean()
    print(f"   phase: longitudes lean towards {np.degrees(np.angle(lean)):+.0f} deg with strength {abs(lean):.2f} "
          f"(rooks {abs(leanR):.2f}); within 30 deg of 0: {100 * near:.0f}% (rooks {100 * nearR:.0f}%, even spread 17%)")
    levels = collections.Counter(np.round(h[ok], 6))
    levelsR = collections.Counter(np.round(PR[okR, 2], 6))
    top = sum(v for _, v in levels.most_common(10)) / ok.sum()
    topR = sum(v for _, v in levelsR.most_common(10)) / okR.sum()
    zR = wave(R, 1, 1)
    print(f"   rows: {len(levels)} latitude levels, the 10 fullest hold {100 * top:.0f}% "
          f"(rooks {len(levelsR)}, {100 * topR:.0f}%); loudness values of the diagonal wave "
          f"{len(set(np.round(abs(z1) ** 2, 6)))} (rooks {len(set(np.round(abs(zR) ** 2, 6)))})")

lo, hi = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) > 2 else (10, 12)
out = {}
for n in range(lo, hi + 1):
    S = solutions(n)
    Q = len(S)
    rng = np.random.default_rng(n)
    R = np.array([rng.permutation(n) for _ in range(Q)])

    # the best-spreading pair of waves (axes are silent for every one-per-row-and-column board)
    freqs = [(u, v) for u in range(1, n) for v in range(1, n)]
    W = {w: wave(S, *w) for w in freqs}
    best = None
    for i, a in enumerate(freqs):
        for b in freqs[i + 1:]:
            P, ok = hopf(W[a], W[b])
            d = len(np.unique(np.round(P[ok], 5), axis=0))      # solutions with both waves silent get no point
            if best is None or d > best[0]:
                best = (d, a, b)
    choices = {"diagonal": ((1, 1), (1, -1)), "spread": (best[1], best[2])}

    out[n] = {"boards": ["".join(f"{c:x}" for c in s) for s in S], "modes": {}}
    print(f"n = {n}: {Q} solutions")
    index = {tuple(s): i for i, s in enumerate(S)}
    for mode, (a, b) in choices.items():
        P, ok = hopf(wave(S, *a), wave(S, *b))
        PR, okR = hopf(wave(R, *a), wave(R, *b))
        st, distinct = stacks(P[ok])
        stR, distinctR = stacks(PR[okR])
        keys = [tuple(k) if good else None for k, good in zip(np.round(P, 5), ok)]
        apart = np.mean([len({keys[index[t]] for t in images(s)}) / len(set(images(s)))
                         for s in S[:3000] if all(ok[index[t]] for t in images(s))])
        loud = np.sqrt(abs(wave(S, *a)) ** 2 + abs(wave(S, *b)) ** 2).mean()
        loudR = np.sqrt(abs(wave(R, *a)) ** 2 + abs(wave(R, *b)) ** 2).mean()
        print(f"   {mode:8s} waves {a} and {b}: {ok.sum()} placed, {distinct} distinct points (rooks {distinctR}), "
              f"most on one point {st.max()} (rooks {stR.max()}), "
              f"turns and mirrors on different points {100 * apart:.0f}%, "
              f"how loud the two waves are {loud:.2f} (rooks {loudR:.2f})")
        if mode == "diagonal":
            diagonal_extras(S, R, P, PR, ok, okR, index, wave(S, *a))
        out[n]["modes"][mode] = {
            "waves": [list(a), list(b)],
            "points": [None if not good else [round(float(x), 4) for x in p] for p, good in zip(P, ok)],
            "stack": [int(x) for x in np.where(ok, np.r_[st, 0][np.cumsum(ok) - 1], 0)],
            "rooks": np.round(PR[okR], 4).ravel().tolist(),
            "distinct": distinct, "distinctRooks": distinctR,
            "maxStack": int(st.max()), "maxStackRooks": int(stR.max()),
        }

json.dump(out, open("flat_sphere.json", "w"), separators=(",", ":"))
print("\nwrote flat_sphere.json")
