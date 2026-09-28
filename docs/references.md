# References

## Counts and sequences

- OEIS A000170, number of n-queens solutions: https://oeis.org/A000170
- OEIS A002562, solutions up to rotation and reflection: https://oeis.org/A002562
- OEIS A007705, toroidal (doughnut) solutions: https://oeis.org/A007705

## Surveys

- J. Bell, B. Stevens, "A survey of known results and research areas for n-queens", *Discrete
  Mathematics* 309 (2009). https://www.sciencedirect.com/science/article/pii/S0012365X07010394

## Doughnut board

- G. Pólya, "Über die 'doppelt-periodischen' Lösungen des n-Damen-Problems" (1918): toroidal solutions
  exist exactly when gcd(n, 6) = 1. Cited via the survey above.

## Cubes and higher dimensions

- D. A. Klarner, "Queen squares", *Journal of Recreational Mathematics* (1979): n² queens in an n x n x n
  cube when gcd(n, 210) = 1.
- J. D. Cook, "Non-attacking queens in an n by n by n cube" (2025), a readable introduction:
  https://www.johndcook.com/blog/2025/05/02/n-queens-in-3d/
- "Solving the n-Queens Problem in Higher Dimensions", arXiv 2410.17873: https://arxiv.org/abs/2410.17873
- "The n-Queens Problem in Higher Dimensions", arXiv 0712.2309: https://arxiv.org/abs/0712.2309
- Paper on the modular result in all dimensions (PDF): https://www.matem.unam.mx/~strausz/Papers/queens.pdf

## Counting and the queenon

- M. Simkin, "The number of n-queens configurations", arXiv 2107.13460 (2021), *Advances in Mathematics*
  (2023): https://arxiv.org/abs/2107.13460
- P. Nobel, A. Agrawal, S. Boyd, "Computing Tighter Bounds on the n-Queens Constant via Newton's Method",
  *Optimization Letters* (2023), arXiv 2112.03336: https://arxiv.org/abs/2112.03336

## Complexity and search

- I. P. Gent, C. Jefferson, P. Nightingale, "Complexity of n-Queens Completion", *JAIR* 59 (2017):
  completing a partly filled board is NP-complete. https://jair.org/index.php/jair/article/view/11079
- S. Minton, M. D. Johnston, A. B. Philips, P. Laird, "Minimizing conflicts: a heuristic repair method
  for constraint satisfaction and scheduling problems", *Artificial Intelligence* 58 (1992).
- P. Morris, "The breakout method for escaping from local minima", AAAI 1993.

## Tools

- PySAT (python-sat), with the CaDiCaL and Glucose solvers: https://pysathq.github.io/
