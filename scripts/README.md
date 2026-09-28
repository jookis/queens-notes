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
