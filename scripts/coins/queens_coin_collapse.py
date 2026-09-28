"""Scale-free coin field: shift(i,j) = (E[top column | queen at (i,j)] - E[top column]) / (n-1), in board widths.
Resample every board onto the same unit square and compare sizes (data collapse). Also draws a strip of maps."""
import numpy as np, os, zlib, struct
from scipy.ndimage import map_coordinates
def load(n):
    L=open(f'cm_{n}.txt').read().split('\n'); K=np.array([[float(v) for v in l.split()] for l in L[1:1+n*n]]).reshape(n,n,n); return K
G=41; gy,gx=np.mgrid[0:1:G*1j,0:1:G*1j]
fields={}; strength={}
for n in [8,10,11,12,13,14,15,16,17,18]:
    if not os.path.exists(f'cm_{n}.txt') or os.path.getsize(f'cm_{n}.txt')==0: continue
    K=load(n); N=K.sum(2); t=np.arange(n)
    Et=(K*t).sum(2)/np.maximum(N,1); Et0=(K[0].sum(0)*t).sum()/K[0].sum()
    S=(Et-Et0)/(n-1); S[0]=np.nan                            # top row itself is trivial
    Sg=map_coordinates(np.nan_to_num(S),[gy*(n-1),gx*(n-1)],order=1)
    fields[n]=Sg; strength[n]=np.nanmean(np.abs(S[1:]))
    rowprof=[np.nanmean(np.abs(S[r])) for r in range(1,n)]
    print(f"n={n:2d}: mean |shift| {strength[n]:.4f} board widths; by row (row 1 .. last):",[round(v,3) for v in rowprof])
ns=sorted(fields); ref=max(ns)
print(f"\nshape similarity to the largest board (n={ref}), rows below the top 10% only:")
m=gy>0.1
for n in ns:
    a=fields[n][m]; b=fields[ref][m]
    print(f"  n={n:2d}: correlation {np.corrcoef(a,b)[0,1]:+.3f}   size ratio (rms) {np.sqrt(np.mean(a*a))/np.sqrt(np.mean(b*b)):.2f}")
# picture strip
def png(a,fn):
    h,w=a.shape[:2]; raw=b''.join(b'\x00'+a[i].tobytes() for i in range(h))
    ch=lambda tg,d: struct.pack('>I',len(d))+tg+d+struct.pack('>I',zlib.crc32(tg+d)&0xffffffff)
    open(fn,'wb').write(b'\x89PNG\r\n\x1a\n'+ch(b'IHDR',struct.pack('>IIBBBBB',w,h,8,2,0,0,0))+ch(b'IDAT',zlib.compress(raw,9))+ch(b'IEND',b''))
tiles=[]
for n in ns:
    K=load(n); N=K.sum(2); t=np.arange(n); Et=(K*t).sum(2)/np.maximum(N,1); Et0=(K[0].sum(0)*t).sum()/K[0].sum()
    S=(Et-Et0)/(n-1); cell=max(8,240//n); img=np.full((n*cell,n*cell,3),255,np.uint8)
    for i in range(n):
        for j in range(n):
            if i==0: col=np.array([0.85,0.85,0.85])
            else:
                d=np.clip(S[i,j]/0.25,-1,1); w=np.array([0.97,0.97,0.97])
                col=w+(np.array([0.13,0.32,0.75])-w)*(-d) if d<0 else w+(np.array([0.8,0.2,0.15])-w)*d
            img[i*cell:(i+1)*cell-1,j*cell:(j+1)*cell-1]=col*255
    pad=np.full((250-img.shape[0],img.shape[1],3),255,np.uint8) if img.shape[0]<250 else np.zeros((0,img.shape[1],3),np.uint8)
    tiles.append(np.vstack([img,pad])); tiles.append(np.full((250,10,3),255,np.uint8))
png(np.ascontiguousarray(np.hstack(tiles)),'coin_shift_strip.png')
