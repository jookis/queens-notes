use std::env;
use std::fs;
use std::thread;

fn search(n: usize, row: usize, cols: u32, d1: u32, d2: u32, full: u32,
          pos: &mut [usize], heat: &mut [u64], count: &mut u64) {
    if row == n {
        *count += 1;
        for r in 0..n { heat[r * n + pos[r]] += 1; }
        return;
    }
    let mut free = full & !(cols | d1 | d2);
    while free != 0 {
        let b = free & free.wrapping_neg();
        free ^= b;
        pos[row] = b.trailing_zeros() as usize;
        search(n, row + 1, cols | b, ((d1 | b) << 1) & full, (d2 | b) >> 1, full, pos, heat, count);
    }
}

fn solve(n: usize) -> (u64, Vec<u64>) {
    let hs: Vec<_> = (0..n).map(|c| thread::spawn(move || {
        let full: u32 = (1u32 << n) - 1;
        let b = 1u32 << c;
        let mut heat = vec![0u64; n * n];
        let mut pos = vec![0usize; n];
        let mut count = 0u64;
        pos[0] = c;
        search(n, 1, b, (b << 1) & full, b >> 1, full, &mut pos, &mut heat, &mut count);
        (count, heat)
    })).collect();
    let mut heat = vec![0u64; n * n];
    let mut total = 0u64;
    for h in hs {
        let (c, hm) = h.join().unwrap();
        total += c;
        for i in 0..n * n { heat[i] += hm[i]; }
    }
    (total, heat)
}

fn corr(x: &[f64], y: &[f64]) -> f64 {
    let k = x.len() as f64;
    let (mx, my) = (x.iter().sum::<f64>() / k, y.iter().sum::<f64>() / k);
    let (mut c, mut vx, mut vy) = (0.0, 0.0, 0.0);
    for i in 0..x.len() {
        let (a, b) = (x[i] - mx, y[i] - my);
        c += a * b; vx += a * a; vy += b * b;
    }
    if vx * vy > 0.0 { c / (vx * vy).sqrt() } else { 0.0 }
}

fn foldmod(n: usize, heat: &[u64], m: usize) -> f64 {
    let mut obs = vec![0u64; m * m];
    for r in 0..n { for c in 0..n { obs[(r % m) * m + (c % m)] += heat[r * n + c]; } }
    let tot: u64 = heat.iter().sum();
    let rc: Vec<f64> = (0..m).map(|a| (0..n).filter(|r| r % m == a).count() as f64).collect();
    let mut worst = 0.0f64;
    for a in 0..m { for b in 0..m {
        let e = tot as f64 * rc[a] * rc[b] / (n * n) as f64;
        if e > 0.0 { worst = worst.max(((obs[a * m + b] as f64) / e - 1.0).abs()); }
    }}
    worst
}

fn main() {
    let a: Vec<String> = env::args().collect();
    let lo: usize = a.get(1).map(|s| s.parse().unwrap()).unwrap_or(8);
    let hi: usize = a.get(2).map(|s| s.parse().unwrap()).unwrap_or(18);
    let dir = a.get(3).cloned().unwrap_or_else(|| ".".into());
    println!("{:>3} {:>12} {:>5} {:>7} {:>7} {:>7} {:>7} {:>7} {:>7} {:>7}  {:>6} {:>6} {:>6} {:>6} {:>6} {:>6}",
        "n","Q","empt","corner","centre","min","max","cAll","cIn","cRing","m2","m3","m4","m5","m6","m7");
    for n in lo..=hi {
        let t = std::time::Instant::now();
        let (q, heat) = solve(n);
        let mean = heat.iter().sum::<u64>() as f64 / (n * n) as f64;
        let empty = heat.iter().filter(|&&v| v == 0).count();
        let mn = *heat.iter().min().unwrap() as f64 / mean;
        let mx = *heat.iter().max().unwrap() as f64 / mean;
        let mid = n / 2;
        let (mut ea, mut da, mut ei, mut di, mut er, mut dr) =
            (vec![], vec![], vec![], vec![], vec![], vec![]);
        for r in 0..n { for c in 0..n {
            let e = ((n - (r as i64 - c as i64).unsigned_abs() as usize)
                   + (n - (r as i64 + c as i64 - (n as i64 - 1)).unsigned_abs() as usize)) as f64;
            let d = heat[r * n + c] as f64 / mean;
            ea.push(e); da.push(d);
            if r == 0 || c == 0 || r == n - 1 || c == n - 1 { er.push(e); dr.push(d); }
            else { ei.push(e); di.push(d); }
        }}
        let mut fm = [0.0f64; 6];
        for (i, m) in (2..=7).enumerate() { if m < n { fm[i] = foldmod(n, &heat, m); } }
        println!("{:>3} {:>12} {:>5} {:>7.3} {:>7.3} {:>7.3} {:>7.3} {:>7.3} {:>7.3} {:>7.3}  {:>6.4} {:>6.4} {:>6.4} {:>6.4} {:>6.4} {:>6.4}  [{:.1}s]",
            n, q, empty,
            heat[0] as f64 / mean, heat[mid * n + mid] as f64 / mean, mn, mx,
            corr(&ea, &da), corr(&ei, &di), corr(&er, &dr),
            fm[0], fm[1], fm[2], fm[3], fm[4], fm[5], t.elapsed().as_secs_f64());
        let mut s = String::new();
        for r in 0..n {
            for c in 0..n { s.push_str(&format!("{} ", heat[r * n + c])); }
            s.push('\n');
        }
        fs::write(format!("{}/heat_{}.txt", dir, n), s).unwrap();
    }
}
