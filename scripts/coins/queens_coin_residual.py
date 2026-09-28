"""Split the coin shift into the part the direct rules explain and the leftover.
Model, row by row: M[j,t] (queen on square (i,j), top queen in column t) is allowed only if t != j and |t-j| != i
(the top queen does not attack (i,j)). IPF fits M to the observed square totals N[i,j] and top-column totals Q[t].
Shift = E[t | square] - E[t]; leftover = observed shift - model shift, in columns."""
import numpy as np, sys
def load(n):
    L=open(f'cm_{n}.txt').read().split('\n'); return np.array([[float(v) for v in l.split()] for l in L[1:1+n*n]]).reshape(n,n,n)
def analyse(n):
    K=load(n); t=np.arange(n); Q=K[0].sum(0); Et0=(Q*t).sum()/Q.sum()
    N=K.sum(2); Sobs=(K*t).sum(2)/np.maximum(N,1)-Et0; Smod=np.zeros((n,n)); err=0
    for i in range(1,n):
        j=np.arange(n)[:,None]; A=((t[None,:]!=j)&(np.abs(t[None,:]-j)!=i)).astype(float)
        M=A*np.outer(N[i],Q)
        for _ in range(3000):
            M*=(N[i]/np.maximum(M.sum(1),1e-300))[:,None]; M*=(Q/np.maximum(M.sum(0),1e-300))[None,:]
        err=max(err,np.abs(M.sum(1)-N[i]).max()/N[i].max(),np.abs(M.sum(0)-Q).max()/Q.max())
        Smod[i]=(M*t).sum(1)/np.maximum(M.sum(1),1)-Et0
    return Sobs,Smod,Sobs-Smod,err
print(" n   obs mean|shift|  model  leftover  leftover share   margin error   centre-col leftover")
res={}
for n in [12,13,14,15,16,17,18,19]:
    So,Sm,R,e=analyse(n); res[n]=(So,Sm,R)
    cz=np.abs(R[1:,n//2]).max() if n%2 else float('nan')
    a=np.abs(So[1:]).mean(); b=np.abs(Sm[1:]).mean(); c=np.abs(R[1:]).mean()
    print(f"{n:2d}   {a:.3f}           {b:.3f}  {c:.3f}     {c/a:6.1%}          {e:.1e}        {cz:.1e}")
np.savez('coin_residual.npz',**{f'obs{n}':v[0] for n,v in res.items()},**{f'mod{n}':v[1] for n,v in res.items()},**{f'res{n}':v[2] for n,v in res.items()})
n=18; R=res[n][2]
print("\nn=18 leftover in tenths of a column ('.' = under 0.05):")
for i in range(1,n): print(f"  r{i:<3}"+" ".join(f"{int(round(v*10)):>+3d}" if abs(v)>=0.05 else "  ." for v in R[i]))
