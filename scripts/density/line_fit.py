"""Fit log(queen density) as a sum of four line terms: row + column + diagonal + anti-diagonal.

Reads the exact heatmaps heat_<n>.txt (n rows of n counts, written by queens_heat.rs) and reports
how much of the pattern the four line terms explain, and the largest leftover per square.

    python3 line_fit.py            # all heat_*.txt in this folder
"""
import glob, os, re
import numpy as np

H = os.path.dirname(os.path.abspath(__file__))

def load(path):
    rows = [l.split() for l in open(path) if l.strip()]
    a = np.array(rows, dtype=float)
    return a / a.mean()

def fit(a):
    n = a.shape[0]
    i, j = np.indices((n, n))
    groups = [i, j, i - j + n - 1, i + j]          # row, column, diagonal, anti-diagonal
    sizes = [n, n, 2 * n - 1, 2 * n - 1]
    cols = []
    for g, s in zip(groups, sizes):
        m = np.zeros((n * n, s))
        m[np.arange(n * n), g.ravel()] = 1
        cols.append(m)
    X = np.hstack(cols)
    y = np.log(a).ravel()
    coef, *_ = np.linalg.lstsq(X, y, rcond=None)
    res = y - X @ coef
    explained = 1 - res.var() / y.var()
    return explained, np.abs(np.expm1(res)).max()

print(" n   explained by 4 line terms   largest leftover per square")
for path in sorted(glob.glob(f"{H}/heat_*.txt"), key=lambda p: int(re.findall(r"\d+", os.path.basename(p))[0])):
    a = load(path)
    e, worst = fit(a)
    print(f"{a.shape[0]:2d}   {100 * e:6.2f}%                     {100 * worst:5.2f}%")
