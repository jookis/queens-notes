# 2. The doughnut board

Glue the left edge of the board to the right and the top to the bottom. Rows and columns are unchanged,
but diagonals now wrap around, so queens attack more. Scripts: `scripts/torus/`.

## Counts **[rerun]** **[known]**

Every doughnut solution is also a flat solution, never the reverse:

```
board   flat   doughnut
  5       10       10
  7       40       28
  8       92        0
 11     2680       88
 13    73712     4524
```

**Doughnut solutions exist exactly when n shares no factor with 6** (Pólya, 1918). So 8x8 has none.

## The rotation rule **[known]**

Put the queen of row r in column (a·r + k) mod n. This is a doughnut solution exactly when a, a − 1 and
a + 1 are all coprime to n: the queen moves a squares sideways per row, which is a step of a − 1 along one
diagonal and a + 1 along the other. With a = 2 this needs n coprime to 6.

These are the **linear** (or "clean") solutions. At a prime size p there are p − 3 usable steps a and p
offsets k, so p(p − 3) clean boards (88 at 11, 130 at 13).

**At 11 every doughnut solution is clean. At 13 most are not: 130 clean, 4394 not** **[rerun]**. This
matters for the cube in [part 3](3-cubes.md).

For flat boards the rotation rule gives an instant solution for any n coprime to 6. A related construction
(odd columns, then even columns) works for every n with n mod 6 not 2 or 3, rechecked for all such
n from 4 to 2000. The other sizes need known small repairs.

## Where the primes come from **[argument]**

The condition "coprime to 6" comes from two choices: wrapping the board, which turns "no two queens attack"
into "these steps are invertible mod n", and asking for linear solutions. Invertible mod n means coprime to
n, so primes appear. They are not a property of queens in general: the flat 8x8 board has 92 solutions
even though 8 is "forbidden". The same mechanism governs Latin squares and pandiagonal magic squares.

## Solutions as waves **[rerun]**

Script: `doughnut_waves.py`. Take the 2-D discrete Fourier transform of a board (1 on queens, 0 elsewhere).
"Exactly one queen on every row, column, wrapped diagonal and wrapped anti-diagonal" is the same as
"the transform is exactly zero on four lines of frequencies through the origin", one line per direction.

```
size   doughnut boards   clean   not clean   non-zero frequencies per board
 11          88            88        0        10
 13        4524           130     4394        12 (clean), 96 or 120 (not clean)
```

This view restates the puzzle rather than solving it. It is useful for classifying solutions and for
"no solution" arguments, not as a faster search.

## Link to magic squares **[argument]**

The grid of values (a·x + b·y + k) mod n is a Latin square. It is pandiagonal (every wrapped diagonal holds
every value) exactly when a, b, a + b and a − b are all coprime to n. The positions of each value then
form one doughnut queens solution, so such a square is a stack of disjoint doughnut solutions. The classic
construction of pandiagonal magic squares combines two such Latin squares, which is why it also needs n
coprime to 6.
