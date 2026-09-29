"""What the solutions in one patch of the sphere have in common (diagonal waves, see flat_sphere.py).

The sphere is cut into the same patches as on flat_sphere.html: 24 height bands x 48 longitude slices,
all of equal area. For every patch with at least 20 solutions, and for comparison for random groups of
solutions of the same sizes:

  own map     how far the patch's own density map (only its solutions stacked on the board) is from the
              overall map: half the summed difference per row, 0 = same, 1 = no overlap. Small groups
              differ by chance too, so the random groups set the scale.
  neighbours  how alike the own maps (minus the overall map) of side-by-side patches are, against
              patches picked at random
  shared      the average number of queens two solutions of one patch have in common, and the number of
              squares that every solution of a patch uses
  moves       how often two solutions of one patch are linked by a move of 2, 3 or 4 queens
              (from solution_moves.json), against two solutions picked at random

The same is done for spots (solutions on exactly the same point) with at least 20 solutions.

    python3 sphere_tiles.py            # reads flat_sphere.json and solution_moves.json, seconds
"""
import json
import numpy as np

NB, NL, MIN = 24, 48, 20
sphere = json.load(open("flat_sphere.json"))
moves = json.load(open("solution_moves.json"))
rng = np.random.default_rng(0)

def own_map(S, members):
    n = S.shape[1]
    M = np.zeros((n, n))
    np.add.at(M, (np.tile(np.arange(n), len(members)), S[members].ravel()), 1)
    return M / len(members)

def distance(M, O):
    return 0.5 * np.abs(M - O).sum() / len(M)

def pair_shared(S, members):
    """Average number of queens two different solutions of the group share."""
    n = S.shape[1]
    C = np.zeros((n, n))
    np.add.at(C, (np.tile(np.arange(n), len(members)), S[members].ravel()), 1)
    m = len(members)
    return (C * (C - 1)).sum() / (m * (m - 1)), int((C == m).sum())

def link_rate(groups, linked):
    pairs = links = 0
    for g in groups:
        s = set(g)
        pairs += len(g) * (len(g) - 1) / 2
        links += sum(1 for i in g for j in linked[i] if j in s and j > i)
    return links / pairs

for key in ("10", "11", "12"):
    n = int(key)
    e = sphere[key]
    S = np.array([[int(c, 16) for c in b] for b in e["boards"]])
    Q = len(S)
    assert e["boards"] == moves[key]["solutions"], "the two data files list the solutions in a different order"
    linked = [set() for _ in range(Q)]
    for k in ("2", "3", "4"):
        E = moves[key]["edges"][k]
        for i, j in zip(E[::2], E[1::2]):
            linked[i].add(j); linked[j].add(i)
    all_pairs_rate = sum(len(x) for x in linked) / (Q * (Q - 1))

    pts = e["modes"]["diagonal"]["points"]
    placed = [i for i, p in enumerate(pts) if p is not None]
    P = np.array([pts[i] for i in placed])
    band = np.clip(((P[:, 2] + 1) / 2 * NB).astype(int), 0, NB - 1)
    slice_ = np.clip(((np.arctan2(P[:, 1], P[:, 0]) + np.pi) / (2 * np.pi) * NL).astype(int), 0, NL - 1)
    tile = band * NL + slice_
    spot = np.unique(np.round(P, 4), axis=0, return_inverse=True)[1].ravel()
    O = own_map(S, np.arange(Q))
    base_shared, _ = pair_shared(S, np.array(placed))

    print(f"n = {n}: {Q} solutions, {len(placed)} on the sphere")
    for label, lab in (("patches", tile), ("spots", spot)):
        groups = [np.array(placed)[lab == t] for t in np.unique(lab)]
        groups = [g for g in groups if len(g) >= MIN]
        if not groups:
            print(f"   {label}: none with {MIN} or more solutions"); continue
        sizes = [len(g) for g in groups]
        rand = [rng.choice(placed, size=m, replace=False) for m in sizes]
        d_own = np.mean([distance(own_map(S, g), O) for g in groups])
        d_rand = np.mean([distance(own_map(S, g), O) for g in rand])
        sh = [pair_shared(S, g) for g in groups]
        sh_r = [pair_shared(S, g) for g in rand]
        print(f"   {label} with {MIN}+ solutions: {len(groups)} (holding {sum(sizes)} solutions, largest {max(sizes)})")
        print(f"      own map vs overall map: {d_own:.3f}   random groups of the same sizes: {d_rand:.3f}")
        print(f"      queens two solutions share: {np.mean([s for s, _ in sh]):.2f}   random groups: {np.mean([s for s, _ in sh_r]):.2f}"
              f"   (any two solutions: {base_shared:.2f})")
        print(f"      squares every solution of the group uses: average {np.mean([c for _, c in sh]):.2f}, "
              f"most {max(c for _, c in sh)}   random groups: average {np.mean([c for _, c in sh_r]):.2f}")
        print(f"      two solutions linked by a small move: {100 * link_rate(groups, linked):.2f}%   "
              f"random groups: {100 * link_rate(rand, linked):.2f}%   any two solutions: {100 * all_pairs_rate:.2f}%")
        if label == "patches":
            maps = {t: own_map(S, np.array(placed)[tile == t]) - O for t in np.unique(tile) if (tile == t).sum() >= MIN}
            corr = lambda a, b: np.corrcoef(a.ravel(), b.ravel())[0, 1]
            near = [corr(maps[t], maps[t + 1]) for t in maps if t % NL != NL - 1 and t + 1 in maps]
            keys = list(maps)
            far = [corr(maps[a], maps[b]) for a, b in (rng.choice(keys, 2, replace=False) for _ in range(2000))]
            if near:
                print(f"      own maps of side-by-side patches alike: {np.mean(near):+.2f} ({len(near)} pairs)   "
                      f"patches picked at random: {np.mean(far):+.2f}")
            else:
                print("      no two side-by-side patches both have enough solutions")
