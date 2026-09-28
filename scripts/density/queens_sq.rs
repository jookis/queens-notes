use std::env; use std::thread; use std::f64::consts::PI;
fn rec(n:usize,row:usize,c:u32,d1:u32,d2:u32,full:u32,pos:&mut [usize],h:&mut [u64],m:&mut u64){
    if row==n { *m+=1; let w=2*n-1;
        for j in 0..n { for k in 0..n {
            let dr=j as i64-k as i64; let dc=pos[j] as i64-pos[k] as i64;
            h[(dr+n as i64-1) as usize*w+(dc+n as i64-1) as usize]+=1; }}
        return; }
    let mut f=full&!(c|d1|d2);
    while f!=0 { let b=f&f.wrapping_neg(); f^=b; pos[row]=b.trailing_zeros() as usize;
        rec(n,row+1,c|b,((d1|b)<<1)&full,(d2|b)>>1,full,pos,h,m); }
}
fn main(){
    let a:Vec<String>=env::args().collect();
    let lo:usize=a.get(1).map(|s|s.parse().unwrap()).unwrap_or(12);
    let hi:usize=a.get(2).map(|s|s.parse().unwrap()).unwrap_or(16);
    for n in lo..=hi {
        let w=2*n-1;
        let hs:Vec<_>=(0..n).map(|c0|thread::spawn(move||{
            let full:u32=(1u32<<n)-1; let b=1u32<<c0;
            let mut h=vec![0u64;w*w]; let mut p=vec![0usize;n]; let mut m=0u64; p[0]=c0;
            rec(n,1,b,(b<<1)&full,b>>1,full,&mut p,&mut h,&mut m); (m,h)})).collect();
        let mut h=vec![0u64;w*w]; let mut m=0u64;
        for t in hs { let (c,hh)=t.join().unwrap(); m+=c; for i in 0..w*w { h[i]+=hh[i]; } }
        let sq=|k:i64,l:i64|{ let mut s=0.0f64;
            for dr in 0..w { for dc in 0..w { let v=h[dr*w+dc]; if v==0 {continue;}
                let (x,y)=(dr as i64-(n as i64-1), dc as i64-(n as i64-1));
                s+=v as f64*(2.0*PI*((k*x+l*y) as f64)/n as f64).cos(); }}
            s/(m as f64)/(n as f64) };
        let mut pts:Vec<(f64,f64,i64,i64)>=vec![];
        for k in 0..(n as i64) { for l in 0..(n as i64) {
            if k==0&&l==0 {continue;}
            let kk=if k>n as i64/2 {k-n as i64} else {k};
            let ll=if l>n as i64/2 {l-n as i64} else {l};
            let q=2.0*PI*(((kk*kk+ll*ll) as f64).sqrt())/n as f64;
            pts.push((q,sq(k,l),kk,ll)); }}
        pts.sort_by(|a,b|a.0.partial_cmp(&b.0).unwrap());
        print!("n={:>2} M={:>10}  smallest-q S(q): ",n,m);
        for p in pts.iter().take(6) { print!("[({},{}) q={:.2} S={:.4}] ",p.2,p.3,p.0,p.1); }
        let f:Vec<_>=pts.iter().filter(|p|p.1>1e-9&&p.0<1.6).collect();
        if f.len()>3 { let k=f.len() as f64;
            let (mx,my):(f64,f64)=(f.iter().map(|p|p.0.ln()).sum::<f64>()/k, f.iter().map(|p|p.1.ln()).sum::<f64>()/k);
            let (mut c,mut v)=(0.0,0.0);
            for p in &f { let d=p.0.ln()-mx; c+=d*(p.1.ln()-my); v+=d*d; }
            print!("  alpha={:.2} (n_fit={})",c/v,f.len()); }
        println!();
    }
}
