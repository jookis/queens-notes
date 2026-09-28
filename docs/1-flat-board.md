# 1. The flat board

Place n queens on an n x n board so that no two share a row, column or diagonal. Script:
`scripts/flat/flat_board.py` unless noted.

## Counts and symmetry **[rerun]** **[known]**

```
 n   solutions   doughnut   families   same after half turn   same after quarter turn
 4       2           0          1              2                      2
 5      10          10          2              2                      2
 6       4           0          1              4                      0
 7      40          28          6              8                      0
 8      92           0         12              4                      0
 9     352           0         46             16                      0
10     724           0         92             12                      0
11    2680          88        341             48                      0
12   14200           0       1787             80                      8
```

- "Families" groups solutions that are rotations or reflections of each other. The columns match
  OEIS A000170 (solutions), A002562 (families) and A007705 (doughnut, see [part 2](2-doughnut-board.md)).
- 8x8: the 92 solutions form 12 families, eleven of 8 and one of 4. The family of 4 is unchanged by a
  half turn.
- **Quarter-turn symmetry needs n ≡ 0 or 1 (mod 4)** **[argument]**. A quarter turn about the centre moves
  every square through a cycle of four, except the centre square on odd boards. So symmetric queens come
  in groups of four, plus at most one in the centre. The condition is necessary but not sufficient: 8 and
  9 pass it and still have none.

## The 92 stacked on one board **[rerun]**

Counting how many of the 92 solutions use each square:

```
 4  8 16 18 18 16  8  4
 8 16 14  8  8 14 16  8
16 14  4 12 12  4 14 16
18  8 12  8  8 12  8 18
18  8 12  8  8 12  8 18
16 14  4 12 12  4 14 16
 8 16 14  8  8 14 16  8
 4  8 16 18 18 16  8  4
```

The map has the board's full 8-fold symmetry, which is forced because the set of solutions is closed
under rotation and reflection. Corners are used least (4), the middle of each edge most (18), and the
centre (8) less than the average of 11.5. Larger boards are in [part 5](5-density-maps.md).

The two closest distinct 8x8 solutions share 6 of their 8 queens.

## Checking a board with XOR and a count **[rerun]**

Script: `scripts/flat/xor2d.py`. Mark queens as 1 and empty squares as 0. XOR along a line gives 1 when
the line holds an odd number of queens. On its own that can't tell 1 queen from 3. It works once a count
is added:

> For each of the four directions (rows, columns, diagonals, anti-diagonals), count the lines whose XOR
> is 1. The board is valid exactly when every one of these counts equals the number of queens.

Why **[argument]**: each queen sits on exactly one line per direction. A line's parity is at most its
number of queens, and equal only when that number is 0 or 1. So the counts reach the number of queens
only if no line holds two or more.

Checked against the direct test on 340,000 random boards (0 to 16 queens) with no disagreement. Of the
40,320 boards with one queen per row and column, it accepts exactly the 92 solutions. The same rule works
in 3-D with 13 directions ([part 3](3-cubes.md)).

This is a check for a finished board. For building a board, the usual bitmask solver (one mask for
columns and one for each diagonal direction) is still the better tool.

## Multiplying boards **[rerun]**

Take a solution A of size m and a solution B of size k, and replace every queen of A by a copy of B. The
result is an mk x mk board.

```
8 (pattern) x 5 (tile) -> 40x40     920 of 920 valid
5 (pattern) x 8 (tile) -> 40x40       0 of 920 valid
```

**Rule:** the tile must be a doughnut solution ([part 2](2-doughnut-board.md)), and the pattern can be any
solution. Tiles sit side by side, so a diagonal leaving one tile enters the next as if the tile's edges
wrapped around. So any of the 92 works as the pattern, but none works as the tile, because 8x8 has no
doughnut solutions. Similar product constructions appear in the n-queens literature; the original source
has not been tracked down here.

## Not kept from the original notes

Timings of a min-conflicts local search on boards up to 5000 x 5000 were measured once and not saved as
a script, so they are left out. Min-conflicts is the standard method for finding one large solution
quickly (Minton et al., 1992).
