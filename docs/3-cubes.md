# 3. Queens in a cube

Place n² queens in an n x n x n cube so that no two attack along any of the 13 directions: 3 along the
axes, 6 face diagonals and 4 space diagonals. That is the most possible, since every vertical column holds
exactly one queen. Such a placement is a **height map**: each square (x, y) of the base gets one height z.
Scripts: `scripts/cubes/`.

## When clean solutions exist **[known]**

The **clean** (linear) cubes have height z = (a·x + b·y + k) mod n. Klarner showed that complete
placements exist when gcd(n, 210) = 1, i.e. n has no prime factor 2, 3, 5 or 7. It is conjectured that
no other size has one. Smallest case: 11 x 11 x 11, for example z = (2x + 4y) mod 11.

## Counting clean cubes **[rerun]**

Script: `torus/wave_counts.py`. The pair (a, b) must avoid 12 "forbidden stripes": none of a, b, a + b and
a − b may be 0, 1 or −1 mod the prime. At a prime p ≥ 11 that leaves (p − 5)(p − 7) pairs, times p
offsets k:

```
clean cubes at prime size p  =  p(p − 5)(p − 7)          11: 264    13: 624
```

For any n coprime to 210, the number of pairs is n² · ∏ over primes p dividing n of (1 − 5/p)(1 − 7/p).
This matches brute force for every such n up to 149, including 121 and 143.

## Every cube at sizes 11 and 13 is clean

| size | complete cubes | all clean? | how | status |
|---|---|---|---|---|
| 11 | 264 | yes | SAT enumeration with blocking clauses (`cube_enum.py`), proved complete in seconds | **[rerun]** |
| 11 | 264 | yes | separately: tiling the base by 11 disjoint flat solutions (exact cover), then every stacking order | **[single run]**, script not kept |
| 11 | none that is not clean | | SAT query "a complete cube that is not linear" is unsatisfiable (`nonclean.py`) | **[rerun]** |
| 13 | 624 | yes | same query at 13 (`nonclean_long.py`), CaDiCaL | **[rerun]**, see caveat |

So at sizes 11 and 13 there are **no irregular solutions**: every complete cube is a single linear wave.

**Why 11 was easy and 13 needed a solver:** each horizontal layer of a complete cube is a doughnut solution
(part 2). At 11 all doughnut solutions are clean, so the layers can only form clean cubes. At 13 there are
4394 non-clean doughnut boards. The SAT proof shows none of them can ever be a layer of a complete cube.

**Caveat for 13:** the proof rests on one solver (CaDiCaL) and on the encoding. The encoding was sanity
checked (`nonclean_test.py`): it rejects all 1331 linear arrangements at 11 and accepts slightly altered
ones, so it is not vacuous. A second solver (Lingeling) timed out after 45 minutes. An independent check,
for example with a proof certificate (DRAT) or a second solver, would make this solid.

Every 11-cube found is a stack of doughnut layers, each shifted by a fixed step per floor (a
"staircase"). No irregular stacking order exists.

## No complete 8 x 8 x 8 cube **[rerun]**

Each horizontal layer of a complete cube is a flat solution, and no two layers may share a square (one
queen per vertical column). So an 8x8x8 cube needs 8 of the 92 flat solutions with no square in common.
An exhaustive search (`flat/flat_board.py`) finds at most **6**. So no complete 8x8x8 arrangement exists.
This agrees with the conjecture above; whether this argument is in the literature has not been checked.

Exhaustive search also finds no complete placement for sizes 2 to 6 **[single run]**.

## Which symmetries a complete cube can have **[rerun]**

Script: `all_syms.py`. The cube has 47 non-trivial turns and mirrors. Each was added as a constraint and
given to a SAT solver. Same result at 11 and 13:

```
quarter turn about an axis              x6   impossible
half turn about an axis                 x3   impossible
third of a turn about a long diagonal   x8   impossible
half turn about a face diagonal         x6   impossible
mirror in a plane                       x9   impossible
turn-and-mirror, order 4 and 6          x14  impossible
point reflection through the centre     x1   possible
```

Short proofs for the turns at every size **[argument]**:

- **Turn about an axis.** A complete placement has exactly one queen on every line along each axis. A
  quarter or half turn about the vertical axis maps the four corner columns onto each other and keeps
  heights, so their four queens share a height. Two of them then share an edge line (quarter turn) or a
  face diagonal (half turn).
- **Third of a turn about a long diagonal**, (x, y, z) → (y, z, x). Column (x, x) holds a queen at
  (x, x, z), which maps to (x, z, x). That lies on the same face diagonal unless z = x. So all n of these
  queens sit on the long diagonal, where they attack each other.
- **Half turn about a face diagonal:** column (x, x) maps to itself with height n − 1 − z. So every such
  queen sits at the middle height, all on one face diagonal.

**Point reflection** (x, y, z) → (n−1−x, n−1−y, n−1−z) is possible. For a clean cube it requires
2k ≡ a + b − 1 (mod n), which always has a solution for odd n. So every clean cube can be shifted into
a point-symmetric position. Example at 11: z = (2x + 4y + 8) mod 11.

## XOR check in 3-D **[rerun]**

Script: `xor3d.py`. The flat-board check (part 1) works unchanged with 13 directions. All 264 (size 11)
and 624 (size 13) cubes pass. Clean cubes with one column moved, random height maps and random sparse
sets all agree with the direct test.

## Local search with "observers" **[single run]**

Scripts: `observers.py`, `observers_fair.py`, `alive_beams.py`. Min-conflicts search on height maps,
guided by conflict counts along each direction. Six runs per case, 60,000 steps:

```
                                  size 11   size 13
4 horizontal directions only        0/6       0/6
all 13 directions                   6/6       0/6
```

The looser puzzle (horizontal directions only) was harder for local search. That is surprising but based
on only 6 runs. Weighting stubborn conflicts (Morris's "breakout" method) did not help. At 13 only the SAT
solver succeeded.

## Cleanness seen as a wave **[rerun]**

Script: `torus/wave.py`. Give each square the complex number exp(2πi·z/n). The 2-D Fourier transform of a
clean cube is a single point at (a, b). Change one square's height and all 169 frequencies light up. A
single point means clean, a spread means not clean.
