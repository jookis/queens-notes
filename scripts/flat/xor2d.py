import itertools, random
# Flat 8x8 board, queens = 1: per direction, count the lines whose XOR (parity) is 1; the board is valid
# exactly when every count equals the number of queens. Checked against the exact "no line holds two" test.
n = 8
bit = lambda r, c: 1 << (r * n + c)
def fam(cells_of_line): return [sum(bit(r, c) for r, c in L) for L in cells_of_line]
dirs = {"rows": fam([[(r, c) for c in range(n)] for r in range(n)]),
        "columns": fam([[(r, c) for r in range(n)] for c in range(n)]),
        "diagonals": fam([[(r, r - k) for r in range(n) if 0 <= r - k < n] for k in range(-n + 1, n)]),
        "anti-diagonals": fam([[(r, k - r) for r in range(n) if 0 <= k - r < n] for k in range(2 * n - 1)])}
pop = lambda x: bin(x).count("1")
def xor_test(B):
    q = pop(B); return all(sum(pop(B & m) & 1 for m in ms) == q for ms in dirs.values())
def exact_test(B):
    return all(pop(B & m) <= 1 for ms in dirs.values() for m in ms)
rnd = random.Random(7); disagree = 0; tried = 0
for k in range(0, 17):
    for _ in range(20000):
        B = sum(bit(*divmod(s, n)) for s in rnd.sample(range(64), k)); tried += 1
        disagree += xor_test(B) != exact_test(B)
perms = [sum(bit(r, c) for r, c in enumerate(p)) for p in itertools.permutations(range(n))]
print(f"random boards with 0..16 queens: {tried:,} tried, XOR+count test disagrees with exact test on {disagree}")
print(f"all 40,320 one-per-row-and-column boards: XOR+count test passes {sum(map(xor_test, perms))} (true solutions: {sum(map(exact_test, perms))})")
row3 = bit(0, 0) | bit(0, 3) | bit(0, 6)
print(f"row with 3 queens: XOR of the row = {pop(row3) & 1}, but rows' XOR count = {sum(pop(row3 & m) & 1 for m in dirs['rows'])} vs 3 queens -> caught")
# Measured 2026-09-13: 340,000 tried, 0 disagreements; passes 92 of 40,320 (true 92).
