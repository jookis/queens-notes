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

## Counts alone are too few **[argument]**

Only about 27 exact values of Q(n) are known. Fitting a smooth growth law to n = 8 to 15 leaves small,
patternless residuals, and the fitted parameters are poorly determined. So the known counts can check a
proposed exact formula but are too few to discover one. No exact formula for Q(n) is known, and none is
expected. A linear fit of ln(Q(n)/n!) against n for n = 10 to 15 does read back α ≈ 1.94 **[single run]**,
a nice consistency check on Simkin's result, though the value moves between 1.9 and 2.0 with the fit range.
