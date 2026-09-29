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

## Solutions on a sphere (Hopf map) **[single run]**

Script: `hopf_sphere.py`, picture: `hopf_sphere.html`. Shifting a doughnut solution along the rows or
columns gives another solution. A shift leaves the size of each wave F(u, v) unchanged and only turns
its phase. Call a solution together with all its shifts a **kind**. At 13 the 4524 solutions fall into
36 kinds: 10 clean (13 shifts each) and 26 not clean (169 shifts each).

The Hopf map takes two complex numbers (z1, z2), scaled to length 1, to a point on an ordinary sphere
and forgets their shared phase. The idea was to use it to fold away the shifts, so that each kind
becomes one point.

- **Two arbitrary waves do not work.** With z1 = F(1, 2) and z2 = F(1, 3) a shift turns the two phases
  by different angles, so only some shifts are folded away. Each non-clean kind is spread over 13
  points.
- **A wave and its double do.** With z1 = F(w)² / n and z2 = F(2w), every shift turns both phases by the
  same angle. Every kind lands on exactly one point (up to rounding, 10⁻¹⁵). The quantity behind it,
  F(w)² times the conjugate of F(2w), is known in signal processing as the bispectrum, so the method is
  not new. The sphere is a way to draw it.
- **The kinds come apart.** With w = (1, 2), 25 kinds get a point, on 23 distinct points. Two pairs
  share a point by coincidence of values; they are not related by any symmetry of the board. Using
  two frequencies together, every kind that is shown gets its own point (28 of 36; with five
  frequencies, 31 of 36).
- **Clean kinds are mostly invisible.** A clean solution sounds on only one line of frequencies, so
  each frequency shows at most one clean kind. A single frequency shows 24 to 26 of the 26 non-clean
  kinds. With the five frequencies together all 26 get a point, and the 5 kinds never shown are all
  clean.
- **Only shifts are folded away, unless the frequency is special.** Turning, mirroring or scaling the
  board ((r, c) → (m·r, m·c)) maps solutions to solutions and groups the 36 kinds into 7 families
  (3 clean, 4 not clean). For w = (1, 2), (1, 3) and (1, 4) related kinds land on different points
  (0 of 88 pairs share one). But w = (1, 5) and (2, 3) are left unchanged by a quarter turn combined
  with a scaling, and there 7 pairs of related kinds share a point. So choosing the frequency also
  chooses which extra symmetry is folded away.

Unlike the stacked density maps, nothing is averaged here: each kind keeps its own point.

## Link to magic squares **[argument]**

The grid of values (a·x + b·y + k) mod n is a Latin square. It is pandiagonal (every wrapped diagonal holds
every value) exactly when a, b, a + b and a − b are all coprime to n. The positions of each value then
form one doughnut queens solution, so such a square is a stack of disjoint doughnut solutions. The classic
construction of pandiagonal magic squares combines two such Latin squares, which is why it also needs n
coprime to 6.
