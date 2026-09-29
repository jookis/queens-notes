# Scripts

Run each script from its own folder, since several read data files or import helpers next to them. The
code is exploratory and written for quick checks, not as a library.

## Setup

```bash
# Python: numpy for most scripts, scipy for queens_coin_collapse.py, python-sat for the SAT proofs
python3 -m venv .venv && .venv/bin/pip install numpy scipy python-sat
```

C programs: `cc -O2 -o prog prog.c`. Rust programs: `rustc -O prog.rs`.

## flat/ (part 1)

| script | what it does | runtime |
|---|---|---|
| `flat_board.py` | counts, families, symmetric boards, 8x8 overlay, largest disjoint set of the 92, board products | seconds |
| `xor2d.py` | XOR-and-count board check against the direct test | seconds |

## torus/ (parts 2 and 3)

| script | what it does |
|---|---|
| `doughnut_waves.py` | all doughnut boards at 11 and 13, split into clean and not clean, with their Fourier "quiet lines" |
| `wave.py` | Fourier picture of a clean 13-cube, and of the same cube with one square changed |
| `wave_counts.py` | allowed wave pairs against the formula, for every n coprime to 210 up to 149 |
| `hopf_sphere.py` | 13x13 doughnut solutions on a sphere: the Hopf map of a wave and its double, one point per solution up to shifts; writes `hopf_sphere.json` for `hopf_sphere.html` (serve the folder with `python3 -m http.server` to view) |

## cubes/ (part 3), needs python-sat

| script | what it does | runtime |
|---|---|---|
| `nonclean_lib.py` | builds the complete-cube CNF and the "not linear" constraint | (helper) |
| `nonclean_test.py` | sanity checks that the "not linear" query is not vacuous | seconds |
| `nonclean.py` | "a complete cube that is not linear" at 11 (proved impossible) and 13 (budgeted) | minutes |
| `nonclean_long.py cadical195` | the full size-13 proof; `lingeling` also works as argument | ~25 min |
| `cube_enum.py` | enumerates complete cubes with blocking clauses: all 264 at 11, a budgeted sample at 13 | ~6 min |
| `all_syms.py` | which of the 47 turns and mirrors a complete cube can have, at 11 and 13 | seconds |
| `diag_turn.py` | the third-of-a-turn case on its own | seconds |
| `point_reflection.py` | finds a point-symmetric complete 11-cube | seconds |
| `xor3d.py` | the XOR-and-count check with 13 directions | seconds |
| `observers_fair.py <n> <full\|horizontal> <steps> <seeds>` | local search guided by conflict counts (uses `run()` from `observers.py`) | minutes |
| `alive_beams.py <n> <full\|horizontal> <steps> <seeds> <noise>` | the same with conflict weighting | minutes |

`results/` holds the outputs of the long runs.

## dimensions/ (part 4)

| script | what it does |
|---|---|
| `dims.py` | exhaustive search: which sizes allow a linear solution in 3-D and 4-D |
| `powers.py` | the binary construction 1, 2, 4, ... checked for every size below 60 |
| `dim5.py` | the boundary check in 5-D |
| `dimcounts.py` | exact linear-solution counts per dimension and size, written to `dimcounts.json` |

## density/ (part 5)

| program | what it does | runtime |
|---|---|---|
| `queens_heat.rs` | `queens_heat <lo> <hi> [dir]`: exact density maps, written as `heat_<n>.txt` | n = 18: ~2 min, n = 20: ~2 h |
| `line_fit.py` | fits the maps with row, column and two diagonal terms | seconds |
| `queens_sq.rs` | `queens_sq <lo> <hi>`: structure factor from all queen pairs | n = 15: seconds |
| `aligned_heat.py [lo hi]` | turns each solution before stacking, per-family and 4-class maps, checked against random rooks; writes `aligned_heat.png` | n = 8 to 12: ~1.5 min |
| `solution_plane.py [lo hi]` | one dot per solution family (multidimensional scaling of queen differences), against random rooks; writes `solution_plane.json` for `solution_plane.html` (serve the folder with `python3 -m http.server` to view) | n = 8 to 12: ~45 s |
| `solution_moves.py [lo hi]` | moves of 2, 3 and 4 queens between solutions: connected groups, flexibility map, shortest paths; writes `solution_moves.json` for `solution_moves.html` | n = 8 to 12: ~10 s |
| `corner_room.py` | why corner queens move more often: open squares per queen, and for swaps the partner's return square, corner vs inside; reads `solution_moves.json` | seconds |
| `classes_vs_moves.py` | the 4 learned classes of `aligned_heat.py` against the moves: how flexible each class is, and how many moves stay inside a class; reads `solution_moves.json` | ~1 min |
| `classes_in_order.py` | the 4 classes along the list of 12x12 solutions in search order: runs, mirror palindrome, first-row blocks, repeats, against shuffled lists | ~30 s |
| `classes_across_n.py` | do the 4 classes come back at other sizes: class maps of n = 10 to 13 compared with turns (and shifts), against random-rook classes | ~10 min |
| `flat_sphere.py [lo hi]` | each flat solution on its own spot of a sphere (Hopf map of two waves, measured from the board centre), diagonal waves and the most spread-out pair, against random rooks; mirror checks, phase lean and height rows; writes `flat_sphere.json` for `flat_sphere.html` (sphere, unrolled map, and a pulsing view of one patch) and for `pulse_map.html` (the ordinary density map with the solutions blinking over it) | n = 10 to 12: ~2 min |
| `sphere_tiles.py` | what the solutions in one patch of the diagonal sphere have in common: small-move links, shared queens, own maps, against random groups; reads `flat_sphere.json` and `solution_moves.json` | seconds |
| `queens_semi_heat.c` | `queens_semi_heat <n> <mode> > semi_heat_<n>_<mode>.txt`: mode 1 semi-queens (one diagonal family), mode 2 ordinary queens | |

`run_19_20.txt` is the console output of the n = 19 and 20 runs.

## coins/ (part 5)

| program | what it does |
|---|---|
| `queens_coinmap.c`, `queens_coinmap_half.c` | `<n> > cm_<n>.txt`: counts solutions by (square, top-row column). The half version uses the mirror symmetry and gives identical tables in half the time |
| `queens_coin_residual.py` | splits the top-row shift into the direct-rule part and the leftover |
| `queens_coin_collapse.py` | compares the shift maps across sizes and draws them as a PNG strip |
| `queens_topbot.c` | `<n> > queens_topbot_<n>.txt`: joint counts of top-row and bottom-row columns |
| `queens_topbot_residual.py` | how much of the top-bottom link the direct rules explain |

The data files are included (coin tables n = 8 to 19, top-bottom tables to 18), so the Python scripts run without redoing the enumeration.
