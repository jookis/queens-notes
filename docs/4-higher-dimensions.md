# 4. Higher dimensions

In D dimensions, place n^(D−1) queens on the wrap-around cube of side n: one queen on every line along
the last axis, with no two attacking along any of the (3^D − 1)/2 directions. A **linear** solution puts
the queen at

    last coordinate = c₁x₁ + c₂x₂ + … + c_(D−1)x_(D−1) + k   (mod n)

Scripts: `scripts/dimensions/`.

## The rule **[known]**

A linear solution exists exactly when **every prime factor of n is at least 2^D**, i.e. n is coprime to
every prime below 2^D:

```
D   forbidden primes            product    first good size
2   2, 3                              6         5
3   2, 3, 5, 7                      210        11
4   2, 3, 5, 7, 11, 13            30030        17
5   all primes below 32            ...         37
```

For D = 3 this is Klarner's result (part 3). The general form, "coprime to all primes up to 2^D − 1",
appears in the sources listed in the [references](references.md). Some secondary sources state it as
gcd(n, (2D − 1)!) = 1, which is a different and incorrect condition (for D = 3, 5! = 120 misses the
prime 7).

Checked by exhaustive search over coefficients (`dims.py`, D = 2 and 3 up to n = 45, D = 4 up to 30) and
by the construction below (`powers.py`, up to n = 60) **[rerun]**.

## A short proof **[argument]**

Write the coefficients as the set C = {c₁, …, c_(D−1), −1}, where −1 belongs to the last coordinate.
Two queens attack along a direction v ∈ {−1, 0, 1}^D exactly when the combination Σ vᵢcᵢ is not a
unit mod n. So the rule is:

> every non-zero combination of the D coefficients with weights −1, 0, +1 must be coprime to n.

Such a combination is the difference of two disjoint sub-sums of C. So the condition says: **all 2^D
subset sums of C are different modulo every prime factor p of n.**

- **Necessary (pigeonhole).** There are 2^D subset sums and only p remainders mod p. If p < 2^D, two of
  them must be equal, whatever the coefficients. So every prime factor must be at least 2^D.
- **Sufficient (binary).** Take the coefficients 1, 2, 4, …, 2^(D−1) (up to sign). Their subset sums are
  exactly 0, 1, …, 2^D − 1, each once, by uniqueness of binary representation. All differences are then
  smaller than 2^D in size, and non-zero, so no prime p ≥ 2^D divides them.

This covers every n, not only primes. The 2^D is simply the number of subsets of D things, or the number
of corners of a D-dimensional cube.

## A direct construction **[rerun]**

For every allowed size, this is a solution with no search:

    last coordinate = 2x₁ + 4x₂ + … + 2^(D−1)x_(D−1) + k   (mod n)

In 2-D this is the familiar "column = 2 × row" rule. In 3-D it is z = 2x + 4y + k.

## What this does not settle **[open]**

The rule is about **linear** solutions. A linear solution on the wrap-around cube is also valid in the
ordinary cube with edges, so the rule always gives solutions there too. What happens without linearity:

- **2-D:** flat boards have non-linear solutions at every size from 4 (8x8 has 92). On the doughnut board
  there are none unless n is coprime to 6 (Pólya).
- **3-D:** it is conjectured that the ordinary cube has no complete placement unless gcd(n, 210) = 1.
  [Part 3](3-cubes.md) confirms this for n = 8 and n = 2 to 6, and finds that at 11 and 13 no non-linear
  solutions exist at all.
