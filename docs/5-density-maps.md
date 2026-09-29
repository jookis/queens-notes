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

## The 4 classes and the web **[single run]**

`classes_vs_moves.py` compares the 4 learned classes from "Turning boards before stacking" with the
moves from `solution_moves.json`, for n = 11 and 12.

- **The classes are not the flexible kind or the corner kind.** Every class is about equally
  flexible: 8.0 to 8.4 of the 12 queens can take part in a move of up to 4 queens at n = 12 (6.3 to
  6.8 of 11 at n = 11). The share of solutions with a queen on a corner square does differ between
  classes (5% to 18% at n = 12), but not in a stable way. At n = 11 a different class stands out (28%)
  while the others are near 10%.
- **Moves stay inside a class about twice as often as chance.** At n = 12, 75% of the 2-, 3- and
  4-queen moves join two solutions of the same class, against 35% for random classes of the same sizes.
  At n = 11 it is 66% against 26%. Two other random starts of the class fit give 63% to 69%, again
  about twice chance.
- This is largely expected. A move changes only 2 to 4 queens, so neighbouring solutions look alike,
  and any grouping by where the queens sit tends to keep them together. What it adds is how the
  earlier results fit together: the solutions form one connected web, and the 4 classes are cuts of
  that web into 4 regions that keep neighbours together. The web has no natural seams, so each fit
  cuts it in a different place. That is why the classes were unstable between runs, even though each
  one follows the web.

**Do the classes come back at other sizes?** `classes_across_n.py` fits the 4 classes three times for
n = 10 to 13 and compares the class maps, scaled to the unit square. Classes are matched one to one,
and each class may take its own turn or mirror. A score of 1 means identical maps. Baselines: two fits
at the same n, and classes fitted the same way to random rook placements.

```
 n     two fits at the same n    n vs n+1    queens vs random-rook classes
10            0.35                 0.21
11            0.31                 0.31
12            0.38                 0.41                  0.22
13            0.41                                       0.21
 random rooks, two fits at n = 12: 0.18
```

- The classes come back at the next size about as well as they repeat at the same size (n = 12 vs 13:
  0.41, against 0.38 for two fits at n = 12). That is about twice the rook baseline, so the
  resemblance is real, but it is loose. It is a similar rough layout, not the same sharp pattern.
- It does not break as the board grows. The match improves a little from n = 10 to 13.
- The class sizes do not carry over. The largest class holds 39% to 51% of the solutions at n = 12,
  depending on the fit.
- **Not in another place.** When each class may also shift by up to a quarter of the board, all scores
  jump (n = 12 vs 13: 0.72), but two fits on random rooks then also match at 0.72. With that much
  freedom the search finds a good match even in noise, so it cannot tell a pattern that moved from a
  coincidence. Nothing points to the classes reappearing somewhere else on the board. Where they come
  back, it is in about the same place.
- Only up to n = 13: the fitting code runs out of memory from n = 14 on.

**Do the classes follow a cycle along the list of solutions?** `classes_in_order.py` takes the 14,200
solutions at n = 12 in the order the search finds them (first-row column first, then the second row,
and so on) and compares the class sequence with the same list shuffled.

- **The list is an exact palindrome.** The left-right mirror image of solution i is always solution
  14,201 − i, and it is always in the same class (100%, shuffled: 35%), because a class does not care
  about mirroring. So the class sequence reads the same backwards.
- **Blocks by the first row.** Each column of the top queen has its own class mix: class 1 holds 64% of
  the solutions with the top queen in a corner column, 62% in the two centre columns, but 33% in
  columns 5 and 8. Mirror columns have identical mixes.
- **Only short runs.** The same class repeats for 2.1 solutions in a row on average, against 1.5 for a
  shuffled list.
- **No fixed cycle.** The strongest repeats along the list are half, a third and a quarter of its
  length (7,100, 4,733 and 3,550 solutions), which come from the palindrome and the block pattern. A
  few repeats every 400 to 650 solutions stand out 3 to 5 times above shuffled lists, perhaps the
  lengths of blocks sharing the first two queens (not checked). No short period does (at most 1.3
  times the shuffled level).
- So the classes follow the structure of the search order, not a cycle of their own.

## A heatmap on a sphere **[single run]**

The density map stacks all solutions on the board squares. Here each solution gets its own spot on
a sphere instead (`flat_sphere.py`, picture `flat_sphere.html`). Two waves of the board, F(u, v) as in
[part 2](2-doughnut-board.md), are put through the Hopf map: the height on the sphere is the balance
between how loud the two waves are, and the longitude is their phase difference. The flat board has
no shifts, so nothing is folded away (unlike the doughnut sphere in part 2). Random rook placements
with the same count are the baseline.

```
 n      solutions   diagonal waves (1,1) and (1,-1)             most spread-out pair of waves
                    spots    most on one spot   rooks: spots     waves          spots    rooks
10          724       139          96               696          (1,3) (6,1)      586      696
11         2680       552         212              2659          (1,2) (8,1)     2479     2661
12        14200      2464         168             13284          (1,2) (2,5)    12603    12975
```

- **The diagonal waves pile solutions up.** At n = 12 the 14,200 solutions share only 2,464 spots,
  with up to 168 on one spot, while random rooks get 13,284 spots with at most 29 on one. The diagonal
  waves of queen solutions are also quieter (3.1 against 4.9 for rooks at n = 12). So the diagonal
  rule makes solutions far more alike in these two waves than random boards are. The heat on the
  sphere shows where they pile up.
- **Other waves spread them out.** Searching all pairs of waves, the best pair gives 12,603 spots at
  n = 12, close to the 12,975 for rooks. These waves have no simple meaning, so the picture is harder
  to read.
- **Solutions with no spot.** At n = 11, 88 solutions have both diagonal waves silent and get no spot.
  They are exactly the doughnut solutions: one queen on every wrapped diagonal makes these waves zero
  (the "quiet lines" of part 2).
- The turns and mirrors of a solution mostly land on different spots (64% to 89% with the diagonal
  waves, 96% to 99% with the spread-out pairs).

**What the diagonal sphere looks like.** Phases are measured from the centre of the board, and the
anti-diagonal wave is F(1, −1), the mirror image of the diagonal wave F(1, 1). (Measured from the
corner square, every longitude turns by a fixed angle, 30° at n = 12. On an even board F(1, n − 1)
also differs from F(1, −1) by a sign, which turns every longitude by 180°. So the direction of the
lean below depends on these choices; its strength does not.)

- **Two mirror halves.** Flipping a board top to bottom turns diagonals into anti-diagonals. On the
  sphere this swaps top and bottom and keeps the longitude, an exact reflection through the equator,
  checked for every solution at n = 10 to 12. So the lower half is an exact mirror image of the upper
  half. A half turn of the board keeps the height and reverses the longitude, and a left-right mirror
  does both. Seen while the sphere turns, a ring of spots just above the equator and its mirror image
  just below meet in a figure 8.
- **A dense side where the two waves are in step.** Queen solutions lean towards longitude 0 (the
  diagonal and anti-diagonal wave in step, seen from the centre): strength 0.25 at n = 11 and 0.22 at
  n = 12, with 29% and 23% of solutions within 30° of 0, against 17% for an even spread. Random rooks
  do not lean (strength at most 0.05). At n = 10 there is no lean (0.01). The symmetry forces the
  dense side to be at 0° or 180°. That it is at 0° is the finding.
- **Rows at fixed heights.** Each diagonal wave is a sum of n unit "clock hands", one per queen,
  pointing in one of n fixed directions set by the queen's diagonal. Queens never share a diagonal, so
  the hands spread out and mostly cancel, and the sum takes few values: 54 different loudness values of
  the diagonal wave at n = 12, against 515 for rooks. So the spots sit on few height levels: 311 at
  n = 12, and the 10 fullest levels hold 35% of the solutions (rooks: 7,863 levels, 4%). The unrolled
  map on the page shows them as rows.
- **On even boards the pattern repeats n/2 times around the sphere.** The density map (spots at the
  poles left out, since they have no longitude) was compared with itself after turning it about the
  axis by 1/k of a full turn, for k = 2, 3, 4, 5, 6, 10 and 12 (correlation, 1 = identical):

  ```
   n     best match               other turns              random rooks
  10     1/5 turn (72°): +0.75    all others -0.02 to +0.07     at most +0.04
  11     none                     -0.06 to +0.03                at most +0.04
  12     1/6 turn (60°): +0.83    1/3: +0.72, 1/2: +0.64,       at most +0.07
                                  1/4: -0.06
  ```

  So at 12 x 12 there are 6 equal shapes around the sphere, and at 10 x 10 there are 5. At a glance
  it can look like 4, because a sphere only shows its front half. Each shape above the equator has its
  exact mirror image below. **[open]** Why the repeat is n/2 on even boards and absent at n = 11; the
  hands pointing at multiples of 360°/n make some link to n likely, but this is not worked out.

**What the solutions in one patch have in common.** `sphere_tiles.py` cuts the diagonal sphere into the
same 24 x 48 equal-area patches as the page and looks at every patch with at least 20 solutions (228
patches holding 8,761 solutions at n = 12). Each measure is compared with random groups of solutions of
the same sizes:

```
 n = 12                                         patches    random groups   any two solutions
 two solutions linked by a small move (2-4)      0.27%         0.02%            0.03%
 queens two solutions share                      1.17          1.04             1.04
 squares every solution of the group uses        0             0
 own map vs overall map (0 = same)               0.266         0.231
 own maps of side-by-side patches alike          +0.12   (random patch pairs: +0.00)
```

- **A patch is a neighbourhood of the move web.** Two solutions of the same patch are one small move
  apart about 10 times as often as two random solutions. The same holds for solutions on exactly the
  same spot (0.32% against 0.03%). At n = 11 the factor is about 2.5 (0.33% against 0.13%). At n = 10
  only 6 patches have 20 solutions, and there is no effect.
- **But there is no fixed core.** Solutions of a patch share only a few more queens than random pairs
  (1.17 against 1.04), and no square is used by all solutions of any patch. A patch's own density map
  differs from the overall map only a little more than a random group's does, and side-by-side patches
  are only slightly alike (+0.12).
- So the diagonal waves group solutions that are close in the web of small moves, without pinning any
  particular queen. On the page, a chosen patch pulses through its solutions, each time taking the
  remaining solution with the fewest queens changed, with the moved queens marked, in time with a pulse
  on the sphere. *Correction kept for honesty:* this was first described as keeping each step small. It
  does not: at n = 12 only 4% of the steps change exactly 4 queens and 88% change more than 6, because
  most solutions have no small-move neighbour inside their patch (0.27% of pairs are).
- **When 4 queens change, it is two swaps, not a rotation.** The 4 queens of a 4-queen change keep
  their rows and trade columns, either as a rotation of four or as two separate swaps. Over all 4-queen
  moves at n = 12, 57% are rotations (random trades of 4 columns would give 67%). But among the
  4-queen steps inside sphere patches, 98% are two swaps (93% at n = 10 and 11). **[open]** A guess:
  two swaps can cancel each other's effect on the diagonal waves and keep both boards on one spot,
  which a rotation of four rarely does. *(Scratch run, not in a repo script.)*

## The solutions as Nimblecube hypervectors **[single run]**

A cross-over with the author's other project, **Nimblecube**: an integer-only similarity memory that
stores patterns as 4096-bit "hypervectors" and compares them by Hamming distance (XOR and a count, the
same trick as the board check in [part 1](1-flat-board.md)). The queen solutions make a fully known test
set for it: for every pair of 12 x 12 solutions we know exactly how they differ, and which ones are
small-move neighbours (differ in 2 to 4 queens). `scripts/nimblecube/queens_hdc` encodes all 14,200
solutions with Nimblecube's own library (`nimblecube-core`, used from a `nimblecube` folder next to this
repo) and asks two things: does the distance between codes follow the difference between the boards,
and is the nearest code a real small-move neighbour?

Two encodings: Nimblecube's `FeatureEncoder` (one channel per row, the queen's column as a "graceful"
level, so that neighbouring columns get similar codes), and for comparison an unrelated random code for
every square, bundled with Nimblecube's majority vote.

```
                                         FeatureEncoder    random code per square
 rank correlation of code distance with:
   how many queens differ                    +0.46               +0.94
   how far the queens moved (columns)        +0.98               +0.42
 for the 13,856 solutions with a small-move neighbour:
   nearest code is a real neighbour          61.7%              100%
   a real neighbour in the 10 nearest        87.7%              100%
   (a random guess hits one 0.03% of the time)
```

- **Each encoding measures a different kind of "similar".** The graceful levels make the code distance
  follow how far the queens moved, almost perfectly (0.98). That is what they are built for: in sensor
  data, 41 is close to 42. But in the puzzle, two queens swapping across the board is a small move,
  while several queens each shifting one column is not. So the nearest `FeatureEncoder` code is a real
  neighbour only 62% of the time, although that is still about 2,000 times better than chance.
- **Unrelated codes per square count differing queens**, and then recall is perfect. The code distance
  grows in clean steps: 694 bits for 2 differing queens, 1,026 for 4, 1,947 for all 12.
- For Nimblecube this suggests that the level encoding decides which kind of similarity the memory
  finds: graceful levels for measured quantities, unrelated codes for categories and positions. One
  seed at one board size; it tests the encodings on known data, not Nimblecube on real sensors.

## Counts alone are too few **[argument]**

Only about 27 exact values of Q(n) are known. Fitting a smooth growth law to n = 8 to 15 leaves small,
patternless residuals, and the fitted parameters are poorly determined. So the known counts can check a
proposed exact formula but are too few to discover one. No exact formula for Q(n) is known, and none is
expected. A linear fit of ln(Q(n)/n!) against n for n = 10 to 15 does read back α ≈ 1.94 **[single run]**,
a nice consistency check on Simkin's result, though the value moves between 1.9 and 2.0 with the fit range.
