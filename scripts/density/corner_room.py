"""Why corner queens move more often: a test of the "free short diagonals" explanation.

In every move a queen stays in its row and changes column. It can only land on a square whose two
diagonals are free. So for each queen we count its open squares: the other squares in its row whose
diagonals no other queen of the solution uses. (This ignores that other queens moving at the same
time can free a diagonal, so it is a close guide, not an exact rule.)

The test has four parts:
  1. Do queens with more open squares move more often?
  2. Do corner queens have more open squares?
  3. Compare corner and inside queens that have the same number of open squares. If the corner
     effect is gone, open squares explain it. If it stays, something else is going on.
  4. The partner (swaps only). A swap of the queens in rows r1 and r2 works exactly when both target
     squares are open: (r1, c2) for the first queen and the "return square" (r2, c1) for its partner,
     which lands in the first queen's old column. So for each open square of a queen, check whether
     the partner's return square is open too, corner vs inside, and whether that accounts for the rest.

Corner = the 3 x 3 block in each corner. Inside = not on the border.
Reads solution_moves.json (from solution_moves.py).

    python3 corner_room.py
"""
import json
import numpy as np

data = json.load(open("solution_moves.json"))

def movable_rows(S, edges, kmax):
    Q, n = S.shape
    moved = np.zeros((Q, n), bool)
    for m in range(2, kmax + 1):
        E = np.array(edges[str(m)], dtype=np.int64).reshape(-1, 2)
        for i, j in E:
            d = S[i] != S[j]
            moved[i] |= d; moved[j] |= d
    return moved

def open_board(S):
    """open[q, r, c]: square (r, c) has both diagonals free of every queen of solution q except the one
    in row r. The queen's own square does not count."""
    Q, n = S.shape
    rows = np.arange(n)
    out = np.zeros((Q, n, n), bool)
    for q in range(Q):
        s = S[q]
        d1 = np.bincount(rows - s + n - 1, minlength=2 * n - 1)
        d2 = np.bincount(rows + s, minlength=2 * n - 1)
        for r in rows:
            c = np.arange(n)
            a, b = r - c + n - 1, r + c
            own1, own2 = (a == r - s[r] + n - 1), (b == r + s[r])
            free = (d1[a] - own1 == 0) & (d2[b] - own2 == 0)
            free[s[r]] = False
            out[q, r] = free
    return out

BINS = [(0, 0, "0"), (1, 1, "1"), (2, 2, "2"), (3, 99, "3+")]

for key in sorted(data, key=int):
    n = int(key)
    if n < 10:
        continue
    e = data[key]
    S = np.array([[int(c, 16) for c in s] for s in e["solutions"]])
    Q = len(S)
    OB = open_board(S)
    room = OB.sum(axis=2)
    cols = S
    rows = np.broadcast_to(np.arange(n), S.shape)
    corner = (np.minimum(rows, n - 1 - rows) < 3) & (np.minimum(cols, n - 1 - cols) < 3)
    inside = (rows > 0) & (rows < n - 1) & (cols > 0) & (cols < n - 1) & ~corner
    print(f"n = {n}: {Q} solutions, {Q * n} queens")
    print(f"   open squares per queen: corner {room[corner].mean():.2f}, inside {room[inside].mean():.2f}")
    for kmax in (2, 4):
        mv = movable_rows(S, e["edges"], kmax)
        by_bin = []
        for lo, hi, label in BINS:
            b = (room >= lo) & (room <= hi)
            by_bin.append(f"{label}: {100 * mv[b].mean():4.1f}% ({b.sum():6d})")
        raw = mv[corner].mean() / mv[inside].mean()
        # corner vs inside inside each bin, then averaged with the corner queens' bin weights
        w, ratios = [], []
        for lo, hi, _ in BINS:
            b = (room >= lo) & (room <= hi)
            if (b & corner).sum() and (b & inside).sum() and mv[b & inside].mean() > 0:
                w.append((b & corner).sum())
                ratios.append(mv[b & corner].mean() / mv[b & inside].mean())
        same_room = np.average(ratios, weights=w)
        expected = sum(((room[corner] >= lo) & (room[corner] <= hi)).mean() * mv[(room >= lo) & (room <= hi) & inside].mean()
                       for lo, hi, _ in BINS) / mv[inside].mean()
        print(f"   moves of up to {kmax}: movable by open squares  " + "   ".join(by_bin))
        print(f"      corner vs inside: {raw:.2f}x overall, {same_room:.2f}x at the same number of open squares; "
              f"open squares alone predict {expected:.2f}x")

    # ---- 4. the partner, swaps only ----
    inv = np.argsort(S, axis=1)                      # inv[q, c] = row of the queen in column c
    tries = {"corner": [0, 0], "inside": [0, 0]}     # [open squares, open squares whose return square is open]
    partner_where = {"corner": [], "inside": []}
    can_swap = np.zeros((Q, n), bool)
    for q in range(Q):
        for r in range(n):
            c1 = S[q, r]
            for c2 in np.flatnonzero(OB[q, r]):
                r2 = inv[q, c2]
                ok = OB[q, r2, c1]
                can_swap[q, r] |= ok
                for name, mask in (("corner", corner), ("inside", inside)):
                    if mask[q, r]:
                        tries[name][0] += 1; tries[name][1] += ok
                        if ok:
                            partner_where[name].append(min(r2, n - 1 - r2, c2, n - 1 - c2))
    mv2 = movable_rows(S, e["edges"], 2)
    assert (can_swap == mv2).all(), "swap rule does not match the found swaps"
    pc = tries["corner"][1] / tries["corner"][0]
    pi = tries["inside"][1] / tries["inside"][0]
    # what the corner/inside ratio would be if corner queens had the inside return rate:
    # a queen with m open squares can swap with probability about 1 - (1 - p)^m
    def predicted(p, mask):
        return (1 - (1 - p) ** room[mask]).mean()
    ratio_room_only = predicted(pi, corner) / predicted(pi, inside)
    ratio_both = predicted(pc, corner) / predicted(pi, inside)
    edge_dist = lambda xs: np.bincount(np.minimum(xs, 3), minlength=4) / max(len(xs), 1)
    dc, di = edge_dist(partner_where["corner"]), edge_dist(partner_where["inside"])
    print("   partner test (swaps only; the rule 'both target squares open' matches every swap found):")
    print(f"      return square open, per open square: corner queens {100 * pc:.1f}%, inside queens {100 * pi:.1f}%")
    print(f"      corner vs inside: actual {mv2[corner].mean() / mv2[inside].mean():.2f}x; model with own open squares "
          f"only {ratio_room_only:.2f}x; with the return squares too {ratio_both:.2f}x")
    print(f"      where the partners sit (distance from the edge 0 / 1 / 2 / 3+): corner queens "
          + " ".join(f"{100 * x:.0f}%" for x in dc) + ", inside queens " + " ".join(f"{100 * x:.0f}%" for x in di))
