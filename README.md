# Queen puzzle notes

Explorations of the n-queens puzzle: the flat board, the wrap-around ("doughnut") board, queens in 3-D
cubes and higher dimensions, and what the average solution looks like on large boards.

> **This is a hobby project.** It was worked out for fun by someone who is not a professional
> mathematician. Nothing here has been peer reviewed. **Please check every result before relying on it.**
> Many of the findings turned out to be known results, and those are marked and cited. If you find a
> mistake or an earlier source, an issue is welcome.

## How it was made

The ideas were bounced back and forth with Claude, Anthropic's AI assistant, over many sessions. The
author's part was a visual approach to problem solving: suggesting how to think about the puzzle, such
as rotating boards, wrapping them into doughnuts, stacking them into cubes, or seeing them as waves.
Claude turned those ways of seeing into precise questions, wrote and ran the scripts and SAT proofs,
looked up the literature, pushed back on ideas that did not hold up, corrected mistakes, and wrote these
notes. Several findings turned out to be known results. A few claims were wrong at first and were
corrected, and the corrections are noted where they matter. Before publishing, the scripts were rerun
from a clean copy and the results compared with the notes.

## How to read the claims

Each finding carries one of these labels:

| label | meaning |
|---|---|
| **[rerun]** | Computed by a script in this repo and rerun from a clean copy before publishing. |
| **[known]** | Already in the literature. Re-derived or re-checked here; see the reference. |
| **[single run]** | Computed once and not repeated or independently confirmed. |
| **[argument]** | A short hand proof or reasoning, not machine checked. |
| **[open]** | A question or an idea, not a result. |

"Not found in the literature" always means *not found in a quick search*, never "new".

## Contents

1. [The flat board](docs/1-flat-board.md): the 92 solutions of 8x8, symmetry, a board check using XOR
   and a count, and which boards can be multiplied into bigger ones.
2. [The doughnut board](docs/2-doughnut-board.md): wrap-around edges, the "rotation rule", and the
   solutions seen as waves.
3. [Queens in a cube](docs/3-cubes.md): n x n queens in an n x n x n cube. Complete classification at
   sizes 11 and 13, which symmetries are possible, and why 8 x 8 x 8 is impossible.
4. [Higher dimensions](docs/4-higher-dimensions.md): when a clean solution exists in d dimensions
   (a known theorem), with a short proof for the linear case and a direct construction.
5. [Density maps](docs/5-density-maps.md): exact per-square occupancy for boards up to 20 x 20, and how
   one queen's position affects the rest of the board.
6. [A chessboard lock](docs/6-lock-build.md): a hobby hardware idea.

[References](docs/references.md) lists the papers and sources used.

## Headline results

| result | status |
|---|---|
| A 3-D cube has a complete clean solution exactly when its size is coprime to 210 | **[known]** (Klarner) |
| In d dimensions: every prime factor of the size must be at least 2^d, and binary coefficients 1, 2, 4, ... build a solution | **[known]** rule; short proof here **[argument]** |
| Exactly 264 complete 11x11x11 arrangements, all of the form height = (a*x + b*y + k) mod 11 | **[rerun]** two methods |
| Exactly 624 complete 13x13x13 arrangements, all of that form | **[rerun]**, one SAT solver |
| Clean cubes at a prime size p ≥ 11: p(p−5)(p−7) | **[rerun]** up to 149 |
| No complete 8x8x8 arrangement: at most 6 of the 92 flat solutions are pairwise disjoint | **[rerun]** |
| Of the cube's 47 turns and mirrors, only point reflection through the centre can leave a complete arrangement unchanged | **[rerun]** at 11 and 13; hand proofs for the turns |
| The average board density (n ≤ 20) is almost exactly a product of row, column and two diagonal terms (99.9% at n = 20) | **[rerun]**; the form is expected from known theory |

## Running the scripts

See [scripts/README.md](scripts/README.md). Most scripts are plain Python 3 (some need numpy). The SAT
proofs need `python-sat`, and the large enumerations are small C or Rust programs.

## License

- Text, tables and data files: [Creative Commons Attribution 4.0](LICENSE) (CC BY 4.0). You may reuse
  and adapt them, including commercially, as long as you give credit.
- Scripts in `scripts/`: [MIT](scripts/LICENSE).

The mathematical results themselves are facts and free for anyone to use either way.
