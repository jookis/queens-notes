//! 12x12 queen solutions as Nimblecube hypervectors: does Hamming distance between codes follow the
//! real differences between boards, and does the nearest code find a real small-move neighbour?
//!
//! Each board is encoded with Nimblecube's `FeatureEncoder` (nimblecube-core): 12 channels (rows), 12
//! graceful levels (the column of that row's queen). For comparison, a second encoding gives every
//! square an unrelated random code and bundles the 12 with Nimblecube's `Hv::bundle`. A "small-move
//! neighbour" is another solution that differs in 2, 3 or 4 rows (see solution_moves.py).
//!
//!     cargo run --release        # about half a minute; needs ../nimblecube next to this repo
use nimblecube_core::encode::FeatureEncoder;
use nimblecube_core::hv::{Hv, DIM_BITS};

const N: usize = 12;

fn solutions() -> Vec<[u8; N]> {
    fn go(r: usize, cols: u32, d1: u32, d2: u32, s: &mut [u8; N], out: &mut Vec<[u8; N]>) {
        let full: u32 = (1 << N) - 1;
        if r == N { out.push(*s); return; }
        let mut free = full & !(cols | d1 | d2);
        while free != 0 {
            let b = free & free.wrapping_neg();
            free ^= b;
            s[r] = b.trailing_zeros() as u8;
            go(r + 1, cols | b, ((d1 | b) << 1) & full, (d2 | b) >> 1, s, out);
        }
    }
    let mut out = Vec::new();
    go(0, 0, 0, 0, &mut [0; N], &mut out);
    out
}

fn xorshift(s: &mut u64) -> u64 { *s ^= *s << 13; *s ^= *s >> 7; *s ^= *s << 17; *s }

/// The comparison encoder: every (row, column) gets its own unrelated random code, bundled per board.
fn random_codes(seed: u64) -> Vec<Hv> {
    let mut s = seed | 1;
    (0..N * N).map(|_| { let mut h = Hv::zero(); for w in h.0.iter_mut() { *w = xorshift(&mut s); } h }).collect()
}

fn queens_differ(a: &[u8; N], b: &[u8; N]) -> usize { a.iter().zip(b).filter(|(x, y)| x != y).count() }
fn columns_moved(a: &[u8; N], b: &[u8; N]) -> usize { a.iter().zip(b).map(|(x, y)| (*x as i32 - *y as i32).unsigned_abs() as usize).sum() }

fn ranks(v: &[f64]) -> Vec<f64> {
    let mut idx: Vec<usize> = (0..v.len()).collect();
    idx.sort_by(|&a, &b| v[a].partial_cmp(&v[b]).unwrap());
    let mut r = vec![0.0; v.len()];
    let mut i = 0;
    while i < idx.len() {
        let mut j = i;
        while j + 1 < idx.len() && v[idx[j + 1]] == v[idx[i]] { j += 1; }
        for k in i..=j { r[idx[k]] = (i + j) as f64 / 2.0; }
        i = j + 1;
    }
    r
}
fn spearman(a: &[f64], b: &[f64]) -> f64 {
    let (ra, rb) = (ranks(a), ranks(b));
    let n = ra.len() as f64;
    let (ma, mb) = (ra.iter().sum::<f64>() / n, rb.iter().sum::<f64>() / n);
    let (mut c, mut va, mut vb) = (0.0, 0.0, 0.0);
    for i in 0..ra.len() { c += (ra[i] - ma) * (rb[i] - mb); va += (ra[i] - ma).powi(2); vb += (rb[i] - mb).powi(2); }
    c / (va * vb).sqrt()
}

fn study(name: &str, sols: &[[u8; N]], codes: &[Hv]) {
    let q = sols.len();
    println!("\n== {name} ==");
    // distance preservation on random pairs
    let mut s = 0x9e37_79b9_7f4a_7c15u64;
    let (mut hd, mut qd, mut cd) = (vec![], vec![], vec![]);
    let mut by_q = vec![(0u64, 0u64); N + 1];
    for _ in 0..200_000 {
        let (i, j) = ((xorshift(&mut s) % q as u64) as usize, (xorshift(&mut s) % q as u64) as usize);
        if i == j { continue; }
        let h = codes[i].hamming(&codes[j]) as f64;
        let d = queens_differ(&sols[i], &sols[j]);
        hd.push(h); qd.push(d as f64); cd.push(columns_moved(&sols[i], &sols[j]) as f64);
        by_q[d].0 += h as u64; by_q[d].1 += 1;
    }
    println!("distance between codes vs the boards (200,000 random pairs; rank correlation, 1 = same order):");
    println!("   vs how many queens differ:  {:+.3}", spearman(&hd, &qd));
    println!("   vs how far the queens moved: {:+.3}", spearman(&hd, &cd));
    // small-move pairs, exactly
    let mut move_h = vec![(0u64, 0u64); 5];
    let mut has_neighbour = vec![false; q];
    let mut nbrs: Vec<Vec<u32>> = vec![vec![]; q];
    for i in 0..q { for j in i + 1..q {
        let d = queens_differ(&sols[i], &sols[j]);
        if (2..=4).contains(&d) {
            let h = codes[i].hamming(&codes[j]) as u64;
            move_h[d].0 += h; move_h[d].1 += 1;
            has_neighbour[i] = true; has_neighbour[j] = true;
            nbrs[i].push(j as u32); nbrs[j].push(i as u32);
        }
    }}
    print!("average distance between codes (of {DIM_BITS} bits), by queens that differ: ");
    for d in 2..=4 { print!("{d}: {:.0}  ", move_h[d].0 as f64 / move_h[d].1 as f64); }
    for d in [6, 8, 10, 12] { if by_q[d].1 > 0 { print!("{d}: {:.0}  ", by_q[d].0 as f64 / by_q[d].1 as f64); } }
    println!();
    // nearest code (not itself): is it a real small-move neighbour?
    let with_n: Vec<usize> = (0..q).filter(|&i| has_neighbour[i]).collect();
    let (mut hit1, mut hit10, mut found, mut total) = (0usize, 0usize, 0usize, 0usize);
    let mut best_possible = 0usize;
    for &i in &with_n {
        let mut dist: Vec<(u32, u32)> = (0..q).filter(|&j| j != i).map(|j| (codes[i].hamming(&codes[j]), j as u32)).collect();
        dist.select_nth_unstable(9);
        let mut top: Vec<(u32, u32)> = dist[..10].to_vec();
        top.sort();
        if nbrs[i].contains(&top[0].1) { hit1 += 1; }
        if top.iter().any(|(_, j)| nbrs[i].contains(j)) { hit10 += 1; }
        let k = nbrs[i].len().min(10);
        found += nbrs[i].iter().filter(|j| top.iter().any(|(_, t)| t == *j)).count().min(k);
        total += k;
            best_possible += 1;
    }
    println!("solutions with at least one small-move neighbour: {} of {q}", with_n.len());
    println!("   nearest code is a real small-move neighbour: {:.1}%   (ranking by queens that differ: 100%)",
             100.0 * hit1 as f64 / best_possible as f64);
    println!("   a real neighbour among the 10 nearest codes: {:.1}%", 100.0 * hit10 as f64 / with_n.len() as f64);
    println!("   share of real neighbours found in the 10 nearest (up to 10 each): {:.1}%", 100.0 * found as f64 / total as f64);
    let chance = with_n.iter().map(|&i| nbrs[i].len() as f64).sum::<f64>() / with_n.len() as f64 / (q - 1) as f64;
    println!("   by chance, a random other solution is a neighbour with probability {:.3}%", 100.0 * chance);
}

fn main() {
    let sols = solutions();
    println!("{N} x {N}: {} solutions; codes of {DIM_BITS} bits", sols.len());
    // Nimblecube's FeatureEncoder: 12 channels (rows), 12 graceful levels (columns)
    let enc = FeatureEncoder::<N, N>::new(0x5eed, [(0, N as i32 - 1); N]);
    let feat: Vec<Hv> = sols.iter().map(|s| enc.encode(&core::array::from_fn(|r| s[r] as i32))).collect();
    study("FeatureEncoder (graceful column levels)", &sols, &feat);
    // comparison: an unrelated random code for every square, bundled with Nimblecube's Hv::bundle
    let rc = random_codes(0x5eed);
    let rand: Vec<Hv> = sols.iter().map(|s| {
        let parts: Vec<Hv> = (0..N).map(|r| rc[r * N + s[r] as usize].clone()).collect();
        Hv::bundle(&parts)
    }).collect();
    study("comparison: a random code for every square", &sols, &rand);
}
