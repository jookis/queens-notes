# 5. Density maps: what the average solution looks like

For each square, count how many solutions put a queen there, then divide by the average. This is the
**density map**. It is one-point information: it says where queens tend to be, not how they depend on
each other. Scripts: `scripts/density/` and `scripts/coins/`.

Background **[known]**: Simkin (2021) proved that the number of solutions grows as
Q(n) = ((1 + o(1)) n e^(−α))^n with α ≈ 1.942, using a limit object called the **queenon**, the
large-n density of queens. Nobel, Agrawal and Boyd narrowed α further with convex optimisation. Simkin's
paper already plots the limit density. What this section adds is exact finite-n data and checks against
it.

## Exact maps up to 20 x 20 **[rerun]**

`queens_heat.rs` enumerates every solution and adds up the squares used. Output: `heat_8.txt` to
`heat_20.txt`. Every total matches the known Q(n) (OEIS A000170), up to Q(20) = 39,029,188,884 (about two
hours, multi-threaded). Maps up to 15 were rerun and are identical.

```
 n            Q   corner   centre    max
14       365596    0.455    0.723   1.416
16     14772512    0.472    0.740   1.398
18    666090624    0.465    0.735   1.402
20  39029188884    0.468    0.739   1.399
```

- The shape settles quickly: from about n = 14 the corner, centre and maximum barely move when the map
  is scaled to the unit square.
- **From n = 11 on, the corner is the emptiest square, but it stays well above zero** (about 0.47 of
  the average). There
  is no region the queens avoid entirely, at least up to n = 20. Some related problems (for example
  domino tilings) have "frozen" regions with a sharp boundary. These maps show no sign of one. Finite data
  cannot prove anything about the limit, but it is consistent with a smooth, fully positive queenon.
- Every square is used by some solution for every n from 8 to 20 (checked from the saved maps).

## The map is almost a product of line terms **[rerun]**

Script: `line_fit.py`. Fit log(density) as a sum of four terms, one for each square's row, column,
diagonal and anti-diagonal:

```
 n    explained   largest leftover per square
14     99.54%          3.9%
16     99.75%          2.5%
18     99.87%          2.3%
20     99.93%          1.9%
```

The fit gets better with n. This product form is what a maximum-entropy problem with row, column and
diagonal constraints predicts, and Simkin's queenon problem is of that kind. So it is expected rather than
new. It is a direct check of that form on exact finite-n data, which we did not find in a quick search.

*Correction kept for honesty:* an earlier fit with only the two diagonal terms left a small "edge ripple"
that looked like a new effect. It disappeared once the row and column terms were included.

## Pair structure **[rerun]**

`queens_sq.rs` computes the structure factor S(q) from all pairs of queens. Along the axes it is exactly
zero, forced by one queen per row and column. Along the diagonal direction the smallest-wavenumber value
stays near 0.40 to 0.44 for n = 13 to 16 instead of shrinking. In physics terms the arrangement is
"hyperuniform" along the axes only, not in every direction.

## Semi-queens **[single run]**

`queens_semi_heat.c` in mode 1 blocks rows, columns and only one diagonal family. Maps for n = 12 to 14
(`semi_heat_*.txt`) converge to a tilted gradient: emptiest along the longest blocked diagonal, fullest
in the two corners where the blocked diagonals are shortest. Mode 2 is ordinary queens and reproduces
Q(n).

## How the top queen affects the rest of the board **[rerun]**

`scripts/coins/`. For every square, the tables `cm_<n>.txt` count solutions by (queen on that square,
column of the top-row queen), for n = 8 to 19. From them:

- **Shift:** how far the average top-row column moves when a given square is occupied. Squares just below
  the top row push the top queen to the opposite side. The effect fades within a few rows and comes back
  weakly at the bottom edge. Measured in columns, the average shift stays about 0.26 for n = 16 to 19, so
  it is an edge effect of fixed size.
- **Direct rules vs the rest** (`queens_coin_residual.py`): a model that only knows "the top queen attacks
  this square" (fitted to the same totals) explains about two thirds of the shift. **The leftover levels
  off at 34% of the pattern for n = 18 and 19**. It forms three bands: extra push near the top, a
  reversed pull in the middle rows, and push again near the bottom.
- **Top row vs bottom row** (`queens_topbot.c`, `queens_topbot_residual.py`): the link between the
  top-row and bottom-row columns, beyond the direct rules, falls from 0.33 bits at n = 8 to about
  0.002 bits at n = 16 to 18. It is almost entirely a small-board effect.

Left-right mirror symmetry holds exactly in all these tables (up to rounding), which is a free
correctness check.

## Turning boards before stacking **[single run]**

The plain map stacks all 8 turns and mirrors of every solution, so it is 8-way symmetric by
construction. The idea here was to turn each solution first, as cryo-EM does before averaging images,
and see if a sharper shape appears. `aligned_heat.py` turns each solution into the pose that best fits
the current average and repeats until nothing changes. It also stacks exact families (no symmetry,
half-turn, quarter-turn) and learns 4 classes, each solution picking its best (class, pose).

Aligning always sharpens a map, even for noise, because the poses are chosen to fit. So every number
is compared with random rook placements aligned the same way, and the maps are scored on held-out
families (whole symmetry orbits) as bits per queen saved against guessing:

```
 n  families   plain   aligned   4 classes  |  rooks: aligned  4 classes
10       92    0.004   -0.002     0.134     |         -0.196    -0.046
11      341    0.031    0.080     0.118     |         -0.078    -0.054
12     1787    0.030    0.135     0.279     |         -0.035    -0.048
```

- **No sharp hidden shape.** The aligned maps are a speckle of a few hot squares, where the alignment
  lined up one queen of many solutions. Aligned random rooks look much the same (last column of
  `aligned_heat.png`).
- **But there is some real signal.** On unseen families, aligned queens predict better than the plain
  map and better than aligned noise, and 4 classes do better again, up to 0.28 bits per queen at
  n = 12 out of log2(12) ≈ 3.6. It is small, and it is not visible to the eye.
- **The classes are not stable.** Restarts from different random starts agree only a little more than
  chance (adjusted Rand index about 0.2 to 0.25, against 0.13 to 0.15 for rooks). So the solutions do not
  fall into a few clear families by where their queens sit. They look more like one continuous cloud.
- The symmetric families are tiny (at most 72 boards up to n = 12). Their maps mostly show those few
  boards, not a trend.

## One dot per solution **[single run]**

`solution_plane.py` makes each family (a solution with its turns and mirrors) one dot. The distance
between two families is the number of queens that differ after the best of the 8 turns and mirrors.
The dots are laid out in the plane by classical multidimensional scaling, which keeps large distances
and does not invent clusters. Random rook placements with the same number of families are the baseline.
`solution_plane.html` shows the result with a board preview for each dot.

```
 n  families   plane keeps   nearest family     2-queen    largest group linked at <= 4 queens
               queens rooks  queens rooks       twins      queens        rooks
10       92    16%   13%     3.09   4.53          25         90 of 92        5
11      341     9%    6%     3.12   4.98         115        302 of 341       5
12     1787     4%    3%     2.87   5.13         695       1737 of 1787      5
```

- **No large groups.** The dots form one blob at every size, and the two plotted directions hold only a
  few percent of the spread. A bimodality test on both axes stays below the two-group threshold (0.555)
  for queens and rooks alike. At n = 11 the 12 linear families (column = a·row + b mod n) sit inside the
  blob, not apart from it.
- **But queen solutions sit close together, in a web of small moves.** Queens and rooks have the same
  number of dots in the same space, yet a queen family's nearest neighbour is about 3 queens away,
  against about 5 for rooks. At n = 12, 695 of the 1787 families have a twin that differs only by
  swapping two queens. Linking families that differ in at most 4 queens joins 1737 of them into one
  group. Random rooks stay in groups of at most 5. So the solutions are not scattered at random among
  the rook placements. They form one connected web, which fits the lack of stable classes in the
  previous section.

*Correction kept for honesty:* this web counts a turn or mirror as free and allows any change of up to
4 queens. It was first described as "one web of small moves", but with only 2- and 3-queen changes
between actual solutions it falls apart into thousands of islands (next section).

## The web of small moves **[single run]**

`solution_moves.py` works on actual solutions, with no free turns. A move rearranges the columns of
k queens so that the board is again a solution: a swap (k = 2), a rotation of three (k = 3), or two
swaps at once or a rotation of four (k = 4). `solution_moves.html` shows the flexibility map and lets
you step through the shortest chain of moves between two solutions.

```
 n   solutions   groups (largest) when moves of up to ... queens are allowed
                  2                 3                 4
10        724     612 (3)           392 (12)          17 (708)
11       2680    2128 (6)          1456 (20)         237 (2392)
12      14200   10800 (12)         4988 (675)        369 (13800)
```

- **The web joins up at four queens.** With moves of up to 3 queens the solutions are thousands of
  small islands. With 4-queen moves almost all of them join one group. At n = 12, 16,132 of the
  4-queen moves link different islands, split about evenly between two swaps at once (7,240) and
  rotations of four (8,892).
- **Edge queens are the flexible ones.** For each square, take the solutions with a queen there, and
  the share in which that queen can be part of a move. For swaps only, a border queen can move 1.3 to
  4.4 times as often as an inner one (1.9 at n = 12). For moves of up to 3 queens the ratio is about
  1.4 to 1.7, and with 4-queen moves it drops to 1.03 to 1.16, since then almost every queen can move
  (98% of solutions at n = 12). So the middle of a solution is the rigid part, and the differences
  between solutions start at the edges.
- **Paths are long.** The farthest pair found in the largest group at n = 12 needs 18 moves (at n = 11, 28).
  These come from a two-pass search, so they are lower bounds on the longest shortest path, not the
  exact value.

## Why corner queens move more often **[single run]**

On the flexibility map the four corners stand out. Two explanations were tested
(`corner_room.py`, reading `solution_moves.json`). Corner means the 3 x 3 block in each corner, and
inside means off the border.

**A smaller solution sitting in the corner: no.** A solution with a queen on a corner square is a
solution of the board one size smaller plus that queen (14% of solutions at n = 12). No bigger corner
block ever holds a complete smaller solution for n = 10 to 12. Corner queens are about as movable in
solutions with this nesting as without (n = 12, swaps: 11% vs 14%; moves of up to 4 queens: 76% vs
81%), so nesting is not the cause. *(Scratch run, not in a repo script.)*

**Free short diagonals: part of the answer.** In a move a queen stays in its row, so it needs an open
square there: one whose two diagonals no other queen uses. The short diagonals near the corners are
almost always empty (at n = 12 a diagonal of length 1 is empty in 96% of solutions, the longest one in
19%), so corner queens have more open squares: 1.56 on average against 1.08 inside.

```
 n = 12                        share of queens that can move, by open squares in their row
                                 0        1        2        3+
 swaps only                     0.0%     6.7%    11.7%    19.7%
 moves of up to 4 queens       55.4%    67.9%    74.5%    81.7%

                     corner vs inside:  overall   predicted from open squares   at equal open squares
 swaps only                              2.66x              1.39x                      1.88x
 moves of up to 4 queens                 1.25x              1.06x                      1.18x
```

- Open squares matter a lot. A queen with none never takes part in a swap. This must be so, because
  the partner in a swap never blocks the target square, so it also checks the code.
- But open squares explain only a quarter to a third of the corner effect at n = 11 and 12 (on a log
  scale; at n = 10 it varies between 12% and 43% depending on the move size). Corner and
  inside queens with the same number of open squares still differ by 1.9x for swaps and 1.2x with
  moves of up to 4 queens. n = 10 and 11 look the same (at equal open squares: 1.4x and 2.0x for
  swaps, 1.16x and 1.17x for moves of up to 4 queens).

**The partner: the rest of the answer, for swaps.** A swap of the queens in rows r1 and r2 works
exactly when both target squares are open: (r1, c2) for the first queen, and the "return square"
(r2, c1) for its partner, which moves into the first queen's old column. The script checks that this
rule gives exactly the swaps found. For a corner queen that old column is near the edge, and the
return square is open about twice as often:

```
 n    return square open,          corner vs inside (swaps)
      per open square              actual   own open squares only   own open squares + return square
      corner    inside
10     7.1%      4.6%               1.97x          1.37x                     2.08x
11     9.2%      4.1%               3.12x          1.42x                     3.09x
12     9.3%      4.9%               2.66x          1.42x                     2.66x
```

(The model treats each open square as an independent try with the measured return rate, so a queen
with m open squares can swap with probability 1 − (1 − p)^m.)

- So for swaps the corner effect is accounted for. Both ends of a swap benefit: the corner queen has
  more open squares in its row, and the partner that moves into its old column also more often finds
  that square open. Both are squares near the edge, where the diagonals are short and often empty.
- The earlier guess that corner queens mostly swap with other edge queens is wrong. Their partners are
  *less* often on the edge: at n = 12, 37% of a corner queen's partners stand on the border, against
  62% for an inside queen. An inside queen can mostly swap only with an edge queen. A corner queen can
  swap with queens further in, because the square it gives up is itself easy to take.
- **[open]** Moves of 3 and 4 queens were not broken down this way. There the corner effect is smaller
  (1.2x with moves of up to 4 queens), and other moving queens can free or block a diagonal, so the
  simple rule no longer holds exactly.

## Counts alone are too few **[argument]**

Only about 27 exact values of Q(n) are known. Fitting a smooth growth law to n = 8 to 15 leaves small,
patternless residuals, and the fitted parameters are poorly determined. So the known counts can check a
proposed exact formula but are too few to discover one. No exact formula for Q(n) is known, and none is
expected. A linear fit of ln(Q(n)/n!) against n for n = 10 to 15 does read back α ≈ 1.94 **[single run]**,
a nice consistency check on Simkin's result, though the value moves between 1.9 and 2.0 with the fit range.
