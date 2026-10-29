# Queen puzzle notes

Notes and computations on the n-queens problem: the flat board and the wrap-around ("toroidal") board, queens in
3-D cubes and higher dimensions, the shape of typical solutions on large boards, and how many solutions there are.

**The notes, results and interactive pictures are on the website: [pieceofdiy.com/queens](https://pieceofdiy.com/queens/).**
This repository is a signpost to them.

## Paper

**The fewest and the most toroidal conflicts of an n-queens solution**, Jouko Kines
([ORCID 0009-0005-6990-8863](https://orcid.org/0009-0005-6990-8863)) (2026). Preprint on Zenodo:
[doi:10.5281/zenodo.23755751](https://doi.org/10.5281/zenodo.23755751). The record holds the paper, the scripts and data that reproduce its
computations, and the Lean 4 proofs of its main theorems.

On the torus, two queens of a solution may share a wrapped diagonal; such a pair is a conflict. The paper shows:

- for n >= 4, the fewest conflicts of a solution is 0, 2 or 3, according as neither, exactly one, or both of 2 and 3 divide n;
  in particular no solution has exactly one conflict;
- no solution has exactly 2 conflicts when n >= 5 is prime, and none has exactly 3 when n = 2q with q >= 5 prime;
- no solution has a cycle of conflicts;
- every solution has at most (sqrt5 - 1) n / 2 conflicts; the floor of this bound is the exact maximum for every n
  from 6 to 50 except 10, 13 and 18, at nineteen larger n up to 233 and, through products with toroidal solutions,
  at 221 further n below 10^5, but not at n = 89.

Companion pages: [the fewest and the most conflicts](https://pieceofdiy.com/queens/8-fewest-and-most-conflicts/)
(notes), [the floor atlas](https://pieceofdiy.com/queens/lab/floor_atlas) and
[the board-size dial](https://pieceofdiy.com/queens/lab/size_dial) (interactive).

## Status

Theorems 2 to 5 (for Theorem 5 its no-cycle part) and 17 of the paper, the discrete bound of Remark 18 and the
values of Corollary 19 except n = 18 are formally verified in Lean 4; the paper has not yet been peer reviewed. The other notes
are exploratory and have not been peer reviewed; many of their findings turned out to be known results, and those are
marked and cited. The computations, the literature search and the drafting were done with an AI assistant (Claude, Anthropic); the
author directed the work, chose the checks, and reviewed and corrected the results, as the paper states. Corrections and earlier sources are welcome as issues.

## The notes

1. [The flat board](https://pieceofdiy.com/queens/1-flat-board/)
2. [The doughnut board](https://pieceofdiy.com/queens/2-doughnut-board/)
3. [Queens in a cube](https://pieceofdiy.com/queens/3-cubes/)
4. [Higher dimensions](https://pieceofdiy.com/queens/4-higher-dimensions/)
5. [Density maps: what the average solution looks like](https://pieceofdiy.com/queens/5-density-maps/)
6. [A chessboard lock (build idea)](https://pieceofdiy.com/queens/6-lock-build/)
7. [Solution structure: big boards, pairs, balance and the swap web](https://pieceofdiy.com/queens/7-solution-structure/)
8. [The fewest and the most conflicts](https://pieceofdiy.com/queens/8-fewest-and-most-conflicts/)
- [References](https://pieceofdiy.com/queens/references/)

Every result as a pre-registered question with its answer: [results analysis](https://pieceofdiy.com/queens/results-analysis/).

## Blog posts

- [Seeing the puzzle](https://pieceofdiy.com/blog/2026-09-30-seeing-the-puzzle/)
- [Listening to a cloud](https://pieceofdiy.com/blog/2026-10-01-listening-to-a-cloud/)
- [When the solutions join up](https://pieceofdiy.com/blog/2026-10-02-when-the-solutions-join-up/)
- [A tour of the queens board](https://pieceofdiy.com/blog/2026-10-03-a-tour-of-the-queens-board/)
- [How many n-queens solutions there are](https://pieceofdiy.com/blog/2026-10-03-how-many-n-queens-solutions/)
- [Computing the queens constant](https://pieceofdiy.com/blog/2026-10-06-computing-the-queens-constant/)
- [Board sizes as trigrams](https://pieceofdiy.com/blog/2026-10-09-board-sizes-as-trigrams/)

## Interactive pictures

- [The floor atlas](https://pieceofdiy.com/queens/lab/floor_atlas)
- [The board-size dial, turning](https://pieceofdiy.com/queens/lab/size_dial)
- [The golden dial](https://pieceofdiy.com/queens/lab/golden_dial)
- [Anatomy of a record board](https://pieceofdiy.com/queens/lab/record_anatomy)
- [Doubled and empty diagonals](https://pieceofdiy.com/queens/lab/class_levels)
- [The two-dial sieve](https://pieceofdiy.com/queens/lab/two_dial_sieve)
- [Board sizes: the background](https://pieceofdiy.com/queens/lab/board_size_background)
- [Board sizes as trigrams (dial)](https://pieceofdiy.com/queens/lab/board_size_bagua)
- [One dot per solution family](https://pieceofdiy.com/queens/lab/solution_plane)
- [Pulsing heatmap](https://pieceofdiy.com/queens/lab/pulse_map)
- [The web of small moves](https://pieceofdiy.com/queens/lab/solution_moves)
- [Solutions on a sphere](https://pieceofdiy.com/queens/lab/flat_sphere)
- [Doughnut solutions on a sphere](https://pieceofdiy.com/queens/lab/hopf_sphere)
- [The semi-queen constant](https://pieceofdiy.com/queens/lab/semi_queen_constant)

## Licence

Text under [CC BY 4.0](LICENSE). The Zenodo record (paper, scripts, data and Lean proofs) is under CC BY 4.0, the
record's licence. The other scripts of the notes are under MIT when published.
