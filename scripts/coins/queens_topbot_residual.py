"""Residual top-bottom link after the direct rules: model M = Pt*Pb*allowed, allowed = different column and not the
two opposite-corner pairs (shared main diagonal), fitted by iterative proportional fitting so its margins match exactly.
Residual information = KL(P || M) in bits: the part of the link the direct rules cannot explain."""
import numpy as np, os
print(" n   total link (bits)   explained by direct rules   residual (bits)   residual share   largest cell deviation obs/model")
for n in [8,10,12,14,15,16,17,18]:
    f=f'queens_topbot_{n}.txt'
    if not os.path.exists(f) or os.path.getsize(f)==0: continue
    L=open(f).read().split('\n'); J=np.array([[float(v) for v in l.split()] for l in L[1:n+1]]); P=J/J.sum()
    Pt,Pb=P.sum(1),P.sum(0); I=np.outer(Pt,Pb)
    A=np.ones((n,n)); np.fill_diagonal(A,0); A[0,n-1]=A[n-1,0]=0
    # also (0,0)-(n-1,n-1) same column already; corners (0,n-1) and (n-1,0): top col 0 & bottom col n-1 share the main diagonal
    M=I*A
    for _ in range(500):
        M*=(Pt/M.sum(1))[:,None]; M*=(Pb/M.sum(0))[None,:]
    kl=lambda p,q: np.sum(np.where(p>0,p*np.log(np.where(p>0,p,1)/np.where(q>0,q,1)),0))/np.log(2)
    tot=kl(P,I); res=kl(P,M); R=np.where(M>0,P/np.where(M>0,M,1),1)
    dev=np.abs(np.log(R[A>0])).max()
    print(f"{n:2d}   {tot:.4f}              {tot-res:.4f}                      {res:.4f}           {res/tot:6.1%}          {np.exp(dev):.2f}x")
