import itertools, random, time
from math import gcd
def setup(n):
    inside = lambda p: all(0 <= c < n for c in p)
    bit = lambda p: 1 << ((p[0] * n + p[1]) * n + p[2])
    dirs = [d for d in itertools.product((-1, 0, 1), repeat=3) if d > (0, 0, 0)]      # the 13 directions
    fams = []
    for d in dirs:
        ms = []
        for p in itertools.product(range(n), repeat=3):
            if inside(tuple(p[i] - d[i] for i in range(3))): continue                   # not a line start
            m, q = 0, p
            while inside(q): m |= bit(q); q = tuple(q[i] + d[i] for i in range(3))
            ms.append(m)
        fams.append(ms)
    return bit, fams
def tests(fams):
    pop = int.bit_count
    xor_test = lambda B: all(sum(pop(B & m) & 1 for m in ms) == pop(B) for ms in fams)   # XOR + count
    exact = lambda B: all(pop(B & m) <= 1 for ms in fams for m in ms)
    return xor_test, exact
rnd = random.Random(3)
for n in (11, 13):
    t = time.time(); bit, fams = setup(n); xor_test, exact = tests(fams)
    cube = lambda H: sum(bit((x, y, H[x][y])) for x in range(n) for y in range(n))
    u = lambda v: gcd(v % n, n) == 1
    pairs = [(a, b) for a in range(n) for b in range(n)
             if all(u(v) for v in (a, b, a - 1, a + 1, b - 1, b + 1, a + b, a - b, a + b - 1, a + b + 1, a - b - 1, a - b + 1))]
    clean = [cube([[(a * x + b * y + k) % n for y in range(n)] for x in range(n)]) for a, b in pairs for k in range(n)]
    groups = {"clean cubes (the complete ones)": clean}
    bent = []
    for _ in range(2000):
        H = [[(0) for _ in range(n)] for _ in range(n)]
        a, b = rnd.choice(pairs); k = rnd.randrange(n)
        H = [[(a * x + b * y + k) % n for y in range(n)] for x in range(n)]
        x, y = rnd.randrange(n), rnd.randrange(n); H[x][y] = (H[x][y] + rnd.randrange(1, n)) % n
        bent.append(cube(H))
    groups["clean cube, one bar moved"] = bent
    groups["random bar heights"] = [cube([[rnd.randrange(n) for _ in range(n)] for _ in range(n)]) for _ in range(2000)]
    groups["random sparse (1 to 40 queens)"] = [sum(1 << s for s in rnd.sample(range(n ** 3), rnd.randint(1, 40))) for _ in range(4000)]
    print(f"{n}x{n}x{n}  ({n ** 3} bits per cube, 13 directions)")
    for name, Bs in groups.items():
        xs, es = [xor_test(B) for B in Bs], [exact(B) for B in Bs]
        print(f"   {name:34} {len(Bs):5}  XOR test passes {sum(xs):4}, exact passes {sum(es):4}, disagreements {sum(x != e for x, e in zip(xs, es))}")
    print(f"   ({time.time() - t:.0f} s)")
