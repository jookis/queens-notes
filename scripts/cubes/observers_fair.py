import sys, time
sys.argv, args = sys.argv[:1] + ["0"], sys.argv[1:]
import importlib.util
spec = importlib.util.spec_from_file_location("obs", "observers.py")
src = open("observers.py").read().split("sides, corners")[0]          # reuse run() only
exec(src)
sides, corners = [(1, 0, 0), (0, 1, 0)], [(1, 1, 0), (1, -1, 0)]
tilted = [(1, 0, 1), (1, 0, -1), (0, 1, 1), (0, 1, -1), (1, 1, 1), (1, 1, -1), (1, -1, 1), (1, -1, -1)]
n, which, steps, seeds = int(args[0]), args[1], int(args[2]), int(args[3])
dirs = sides + corners if which == "horizontal" else sides + corners + tilted
t = time.time(); res = [run(n, dirs, steps, 100 + s)[0] for s in range(seeds)]
ok = sorted(r for r in res if r is not None)
print(f"{n}: {which:10} solved {len(ok)}/{seeds} within {steps} steps, steps used {ok}  ({time.time() - t:.0f} s)")
