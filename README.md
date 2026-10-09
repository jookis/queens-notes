# Queen puzzle notes

Hobby explorations of the n-queens puzzle: the flat board, the wrap-around ("doughnut") board, queens in 3-D
cubes and higher dimensions, what the average solution looks like on large boards, and how many solutions
there are.

**Everything lives on the website: [pieceofdiy.com/queens](https://pieceofdiy.com/queens/).** This GitHub
page only points there; the notes, results, scripts' outputs and interactive pictures are kept and updated
on the site.

> This is a hobby project, worked out with Claude (Anthropic's AI assistant) by someone who is not a
> professional mathematician. Nothing here has been peer reviewed. Please check every result before relying
> on it.

## The notes

1. [The flat board](https://pieceofdiy.com/queens/1-flat-board/)
2. [The doughnut board](https://pieceofdiy.com/queens/2-doughnut-board/)
3. [Queens in a cube](https://pieceofdiy.com/queens/3-cubes/)
4. [Higher dimensions](https://pieceofdiy.com/queens/4-higher-dimensions/)
5. [Density maps: what the average solution looks like](https://pieceofdiy.com/queens/5-density-maps/)
6. [A chessboard lock (hobby build idea)](https://pieceofdiy.com/queens/6-lock-build/)
7. [Solution structure: big boards, pairs, balance and the swap web](https://pieceofdiy.com/queens/7-solution-structure/)
- [References](https://pieceofdiy.com/queens/references/)

Every result as a pre-registered question with its answer: [results analysis](https://pieceofdiy.com/queens/results-analysis/)
and the [question list](https://pieceofdiy.com/queens/results-questions/).

## Highlights

- **The queens constant measured:** a Monte Carlo count on 128 x 128 and 256 x 256 boards gives
  e^C = 2.5595 +- 0.0022, siding with the computed 2.560 over the earlier 2.55 (a confirmation run fixed in
  advance). See [A tour of the queens board](https://pieceofdiy.com/blog/2026-10-03-a-tour-of-the-queens-board/).
- **Why 14 x 14 stands out:** three arithmetic gears decide which perfect structures exist on each board size,
  with the Lo Shu and magic squares. See [Board sizes as trigrams](https://pieceofdiy.com/blog/2026-10-09-board-sizes-as-trigrams/).

## Blog posts

- [Seeing the puzzle](https://pieceofdiy.com/blog/2026-09-30-seeing-the-puzzle/)
- [Listening to a cloud](https://pieceofdiy.com/blog/2026-10-01-listening-to-a-cloud/)
- [When the solutions join up](https://pieceofdiy.com/blog/2026-10-02-when-the-solutions-join-up/)
- [A tour of the queens board](https://pieceofdiy.com/blog/2026-10-03-a-tour-of-the-queens-board/)
- [Board sizes as trigrams](https://pieceofdiy.com/blog/2026-10-09-board-sizes-as-trigrams/)

## Interactive pictures

- [One dot per solution family](https://pieceofdiy.com/queens/lab/solution_plane)
- [Pulsing heatmap](https://pieceofdiy.com/queens/lab/pulse_map)
- [The web of small moves](https://pieceofdiy.com/queens/lab/solution_moves)
- [Solutions on a sphere](https://pieceofdiy.com/queens/lab/flat_sphere)
- [Doughnut solutions on a sphere](https://pieceofdiy.com/queens/lab/hopf_sphere)
- [The semi-queen constant](https://pieceofdiy.com/queens/lab/semi_queen_constant)
- [Board sizes as trigrams (dial)](https://pieceofdiy.com/queens/lab/board_size_bagua)

## Licence

Text under [CC BY 4.0](LICENSE). Questions and corrections are welcome as issues here or through the site.
