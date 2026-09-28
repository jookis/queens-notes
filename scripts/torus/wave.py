import numpy as np
N = 13
x, y = np.meshgrid(range(N), range(N), indexing="ij")
def spectrum(H):
    P = np.abs(np.fft.fft2(np.exp(2j * np.pi * H / N))) / N**2       # strength of each wave (a, b)
    return P
clean = (2 * x + 5 * y + 7) % N
print("clean 13-cube, height = 2x + 5y + 7 mod 13, drawn as letters (a=0 ... m=12):")
for r in clean: print("   " + " ".join("abcdefghijklm"[v] for v in r))
P = spectrum(clean)
print("waves present:", [(int(a), int(b), round(float(P[a, b]), 3)) for a, b in zip(*np.nonzero(P > 1e-9))])
messy = clean.copy(); messy[4, 6] = (messy[4, 6] + 3) % N
P = spectrum(messy)
print(f"one square changed: waves present {int((P > 1e-9).sum())} of 169, biggest {P.max():.3f}")
