"""Are the 4 learned classes of aligned_heat.py related to the web of small moves?

Two questions, for n = 11 and 12:
  1. Is one class the flexible kind? Per class: share of solutions with a possible swap, average
     number of queens that can take part in a move of up to 4 queens, share with a queen on a corner
     square, and average number of queens in the corner 3 x 3 blocks.
  2. Do moves stay inside a class? Share of 2-, 3- and 4-queen moves whose two solutions are in the
     same class, against classes drawn at random with the same sizes. Repeated for two other random
     starts of the class fit.

Uses the fitting code of aligned_heat.py (with the same seed as there) and the moves in
solution_moves.json (from solution_moves.py). Both enumerate the solutions in the same order, which is
checked.

    python3 classes_vs_moves.py        # about a minute
"""
import json
import numpy as np

# aligned_heat.py runs its whole study when imported, so take only its functions (everything above
# its "run" marker).
exec(open("aligned_heat.py").read().split("# ---------- run ----------")[0])

data = json.load(open("solution_moves.json"))

for n in (11, 12):
    S = solutions(n)
    Q = len(S)
    Sm = np.array([[int(c, 16) for c in s] for s in data[str(n)]["solutions"]])
    assert (S == Sm).all(), "the two scripts list the solutions in a different order"
    P = poses(S)
    fits = [best_fit(P, K, seed=seed)[0][1] for seed in (100 + n, 7, 8)]   # the script's seed first
    cls = fits[0]

    edges = {k: np.array(data[str(n)]["edges"][k], dtype=np.int64).reshape(-1, 2) for k in ("2", "3", "4")}
    moved2 = np.zeros((Q, n), bool)
    moved4 = np.zeros((Q, n), bool)
    for k, E in edges.items():
        for i, j in E:
            d = S[i] != S[j]
            moved4[i] |= d; moved4[j] |= d
            if k == "2":
                moved2[i] |= d; moved2[j] |= d
    rows = np.arange(n)
    corner_square = np.array([s[0] in (0, n - 1) or s[-1] in (0, n - 1) for s in S])
    in_corner = np.array([((np.minimum(rows, n - 1 - rows) < 3) & (np.minimum(s, n - 1 - s) < 3)).sum() for s in S])

    print(f"n = {n}")
    print("  class   size   can swap   movable queens (up to 4)   corner-square queen   queens in corner 3x3")
    for rank, c in enumerate(np.argsort(-np.bincount(cls, minlength=K))):
        m = cls == c
        print(f"  {rank + 1:5d} {m.sum():6d}   {100 * moved2[m].any(1).mean():6.1f}%   {moved4[m].sum(1).mean():14.2f}"
              f"            {100 * corner_square[m].mean():10.1f}%        {in_corner[m].mean():10.2f}")
    print(f"    all {Q:6d}   {100 * moved2.any(1).mean():6.1f}%   {moved4.sum(1).mean():14.2f}"
          f"            {100 * corner_square.mean():10.1f}%        {in_corner.mean():10.2f}")

    E = np.vstack(list(edges.values()))
    for name, c in zip(("the fit in aligned_heat.py", "another start", "another start"), fits):
        p = np.bincount(c, minlength=K) / Q
        same = (c[E[:, 0]] == c[E[:, 1]]).mean()
        print(f"  moves inside one class, {name}: {100 * same:.1f}%  (random classes of the same sizes: {100 * (p ** 2).sum():.1f}%)")
