"""The web of small moves between solutions: which queens can move, and how one solution turns into another.

A move takes a solution and rearranges the columns of k of its queens (k = 2: swap two queens,
k = 3: rotate three, k = 4: two swaps at once or rotate four) so that the result is again a solution.
Turning or mirroring the board is not a move here. Two solutions are linked by a k-move exactly when
they differ in k rows.

For each n this finds all 2-, 3- and 4-moves and reports:

  groups        how the solutions split into connected groups when moves of up to k queens are allowed
  joining       the 4-moves that link different groups of the "up to 3" web, by kind
  flexibility   for each square: of the solutions with a queen there, the share in which that queen
                can take part in some move (swaps only, up to 3 queens, up to 4 queens)
  path          a far-apart pair in the largest "up to 4" group, and the shortest chain of moves between

    python3 solution_moves.py          # n = 8 to 12, under a minute
    python3 solution_moves.py 8 10

Writes solution_moves.json for solution_moves.html. To view it locally, run `python3 -m http.server`
in this folder and open solution_moves.html.
"""
import sys, json, itertools
from collections import deque
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

def moves(S, k):
    """All pairs (i, j), i < j, of solutions that differ in exactly k rows."""
    Q, n = S.shape
    weights = n ** np.arange(n - k, dtype=np.int64)
    pairs = []
    for rows in itertools.combinations(range(n), k):
        keep = [r for r in range(n) if r not in rows]
        key = S[:, keep] @ weights
        order = np.argsort(key, kind="stable")
        ks = key[order]
        starts = np.flatnonzero(np.r_[True, ks[1:] != ks[:-1]])
        ends = np.r_[starts[1:], Q]
        for a, b in zip(starts, ends):
            if b - a < 2:
                continue
            g = order[a:b]
            for i, j in itertools.combinations(g, 2):
                if (S[i, list(rows)] != S[j, list(rows)]).all():
                    pairs.append((min(i, j), max(i, j)))
    return np.array(pairs, dtype=np.int64).reshape(-1, 2)

def components(Q, edges):
    parent = np.arange(Q)
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    for i, j in edges:
        a, b = find(i), find(j)
        if a != b:
            parent[a] = b
    return np.array([find(x) for x in range(Q)])

def group_summary(lab):
    sizes = np.bincount(np.unique(lab, return_inverse=True)[1])
    return {"groups": int(len(sizes)), "largest": int(sizes.max()), "alone": int((sizes == 1).sum())}

def flexibility(S, edges):
    """Share of solutions with a queen on (r, c) in which that queen takes part in some move."""
    Q, n = S.shape
    moved = np.zeros((Q, n), bool)
    for i, j in edges:
        d = S[i] != S[j]
        moved[i] |= d; moved[j] |= d
    has = np.zeros((n, n)); can = np.zeros((n, n))
    rows = np.arange(n)
    for q in range(Q):
        has[rows, S[q]] += 1
        can[rows[moved[q]], S[q][moved[q]]] += 1
    return can / np.maximum(has, 1), moved.any(axis=1).mean()

def bfs(adj, start):
    dist = {start: 0}; prev = {start: None}; q = deque([start])
    while q:
        x = q.popleft()
        for y in adj[x]:
            if y not in dist:
                dist[y] = dist[x] + 1; prev[y] = x; q.append(y)
    return dist, prev

def far_pair(Q, edges, lab):
    adj = [[] for _ in range(Q)]
    for i, j in edges:
        adj[i].append(int(j)); adj[j].append(int(i))
    big = np.bincount(lab).argmax()
    start = int(np.flatnonzero(lab == big)[0])
    d, _ = bfs(adj, start)
    u = max(d, key=d.get)
    d, prev = bfs(adj, u)
    v = max(d, key=d.get)
    path = [v]
    while prev[path[-1]] is not None:
        path.append(prev[path[-1]])
    return path[::-1]

def kind_of_4move(a, b):
    """'two swaps' or 'rotate four' for two solutions that differ in 4 rows."""
    rows = np.flatnonzero(a != b)
    perm = {a[r]: b[r] for r in rows}
    x, length = a[rows[0]], 1
    while perm[x] != a[rows[0]]:
        x = perm[x]; length += 1
    return "rotate four" if length == 4 else "two swaps"

lo, hi = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) > 2 else (8, 12)
out = {}
for n in range(lo, hi + 1):
    S = solutions(n)
    Q = len(S)
    E = {k: moves(S, k) for k in (2, 3, 4)}
    up3 = np.vstack([E[2], E[3]])
    up4 = np.vstack([up3, E[4]])
    lab2, lab3, lab4 = components(Q, E[2]), components(Q, up3), components(Q, up4)
    g2, g3, g4 = group_summary(lab2), group_summary(lab3), group_summary(lab4)
    joining = [(i, j) for i, j in E[4] if lab3[i] != lab3[j]]
    kinds = {"two swaps": 0, "rotate four": 0}
    for i, j in joining:
        kinds[kind_of_4move(S[i], S[j])] += 1
    flex2, any2 = flexibility(S, E[2])
    flex3, any3 = flexibility(S, up3)
    flex4, any4 = flexibility(S, up4)
    density = np.zeros((n, n))
    for s in S:
        density[np.arange(n), s] += 1
    path = far_pair(Q, up4, lab4)

    print(f"n = {n}: {Q} solutions, moves of 2 / 3 / 4 queens: {len(E[2])} / {len(E[3])} / {len(E[4])}")
    for name, g in (("up to 2", g2), ("up to 3", g3), ("up to 4", g4)):
        print(f"   {name}: {g['groups']:5d} groups, largest {g['largest']:5d}, alone {g['alone']:5d}")
    print(f"   4-moves joining different 'up to 3' groups: {len(joining)} "
          f"({kinds['two swaps']} two swaps, {kinds['rotate four']} rotate four)")
    print(f"   solutions with at least one movable queen: up to 2 {100 * any2:.0f}%, up to 3 {100 * any3:.0f}%, "
          f"up to 4 {100 * any4:.0f}%")
    edge = np.zeros((n, n), bool); edge[[0, -1], :] = True; edge[:, [0, -1]] = True
    for name, f in (("up to 2", flex2), ("up to 3", flex3), ("up to 4", flex4)):
        print(f"   flexibility {name}: border {f[edge].mean():.2f}, inside {f[~edge].mean():.2f}, "
              f"ratio {f[edge].mean() / f[~edge].mean():.2f}")
    print(f"   longest shortest chain found in the largest group: {len(path) - 1} moves")

    out[n] = {
        "solutions": ["".join(f"{c:x}" for c in s) for s in S],
        "edges": {str(k): E[k].ravel().tolist() for k in (2, 3, 4)},
        "groups": {"2": g2, "3": g3, "4": g4},
        "joining": kinds, "joiningCount": len(joining),
        "anyMovable": {"2": any2, "3": any3, "4": any4},
        "flex": {"2": np.round(flex2, 4).tolist(), "3": np.round(flex3, 4).tolist(), "4": np.round(flex4, 4).tolist()},
        "density": np.round(density / density.mean(), 4).tolist(),
        "path": [int(x) for x in path],
    }

json.dump(out, open("solution_moves.json", "w"), separators=(",", ":"))
print("\nwrote solution_moves.json")
