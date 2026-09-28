/* Per square, per top-row column: how many solutions have a queen on that square while the top queen is in that column.
   Output: n, Q, then n*n lines of n counts (row-major squares, counts by top column). */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
static int n, pos[32]; static uint64_t K[32][32][32];
static void go(int r, uint32_t cols, uint32_t ld, uint32_t rd){
    uint32_t all=(1u<<n)-1, avail=all&~(cols|ld|rd);
    if(r==n){ int t=pos[0]; for(int i=0;i<n;i++) K[i][pos[i]][t]++; return; }
    while(avail){ uint32_t b=avail&-avail; avail^=b; pos[r]=__builtin_ctz(b);
        go(r+1, cols|b, ((ld|b)<<1)&all, (rd|b)>>1); }
}
int main(int argc,char**argv){ n=atoi(argv[1]); go(0,0,0,0);
    uint64_t Q=0; for(int j=0;j<n;j++) for(int t=0;t<n;t++) Q+=K[0][j][t];
    printf("%d %llu\n",n,(unsigned long long)Q);
    for(int i=0;i<n;i++) for(int j=0;j<n;j++){ for(int t=0;t<n;t++) printf("%llu ",(unsigned long long)K[i][j][t]); printf("\n"); } }
