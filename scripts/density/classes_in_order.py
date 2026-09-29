"""Do the 4 learned classes of aligned_heat.py follow a cycle along the list of solutions?

The 14,200 solutions of the 12 x 12 board are taken in the order the search finds them (first-row
column first, then the second row, and so on). Along that list, compared with the same list shuffled:

  runs      how long the same class keeps repeating
  mirror    whether a solution and its left-right mirror image sit at mirrored places in the list, and
            are in the same class (then the class list reads the same backwards)
  blocks    the class mix for each column of the first-row queen
  periods   the strongest repeats along the list for each class (Fourier), against shuffled lists

Uses the fitting code of aligned_heat.py with the same seed as there.

    python3 classes_in_order.py        # about half a minute
"""
import numpy as np

# aligned_heat.py runs its whole study when imported, so take only its functions (everything above
# its "run" marker).
exec(open("aligned_heat.py").read().split("# ---------- run ----------")[0])

n = 12
S = solutions(n)
Q = len(S)
(_, cls, _, _, _), _ = best_fit(poses(S), K, seed=100 + n)
rank = np.empty(K, int)
rank[np.argsort(-np.bincount(cls, minlength=K))] = np.arange(K)
cls = rank[cls]                                           # class 1 = the largest
rng = np.random.default_rng(0)
shuffled = [rng.permutation(cls) for _ in range(200)]
print(f"n = {n}: {Q} solutions in search order; class sizes {np.bincount(cls).tolist()}")

runs = lambda c: 1 + int((c[1:] != c[:-1]).sum())
print(f"runs: {runs(cls)} runs of the same class, average length {Q / runs(cls):.1f} "
      f"(shuffled: average length {Q / np.mean([runs(c) for c in shuffled]):.1f})")

index = {tuple(s): i for i, s in enumerate(S)}
mirror = np.array([index[tuple(n - 1 - s)] for s in S])
print(f"mirror: the mirror image of solution i is solution {Q + 1} - i for every i: "
      f"{bool((mirror == Q - 1 - np.arange(Q)).all())}")
print(f"   same class as its mirror image: {100 * (cls == cls[mirror]).mean():.1f}% "
      f"(shuffled: {100 * np.mean([(c == c[mirror]).mean() for c in shuffled]):.1f}%); "
      f"the class list reads the same backwards at {100 * (cls == cls[::-1]).mean():.1f}% of places")

print("blocks: class mix by the column of the first-row queen (class 1 .. 4)")
for c in range(n):
    m = S[:, 0] == c
    print(f"   column {c + 1:2d} ({m.sum():5d} solutions): " + " ".join(f"{100 * (cls[m] == k).mean():5.1f}%" for k in range(K)))

print("periods: the 3 strongest repeats along the list per class, as a multiple of the strongest repeat in")
print("         shuffled lists (99th percentile of 50)")
for k in range(K):
    x = (cls == k).astype(float)
    x -= x.mean()
    F = abs(np.fft.rfft(x)) ** 2
    limit = np.percentile([(abs(np.fft.rfft(rng.permutation(x))) ** 2)[1:].max() for _ in range(50)], 99)
    top = np.argsort(F[1:])[::-1][:3] + 1
    print(f"   class {k + 1}: " + ", ".join(f"every {Q / j:7.1f} solutions ({F[j] / limit:4.1f}x)" for j in top))
