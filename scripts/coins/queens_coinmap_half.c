/* Same output as queens_coinmap.c, using the left-right mirror to halve the work.
   Top queen in column c < n/2: count the solution and its mirror image. Odd n, top queen in the centre column:
   that branch is closed under mirroring, so it is counted once as is. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
static int n, pos[32]; static uint64_t K[32][32][32];
static void go(int r, uint32_t cols, uint32_t ld, uint32_t rd, int mirror){
    uint32_t all=(1u<<n)-1, avail=all&~(cols|ld|rd);
    if(r==n){ int t=pos[0];
        for(int i=0;i<n;i++){ K[i][pos[i]][t]++; if(mirror) K[i][n-1-pos[i]][n-1-t]++; } return; }
    while(avail){ uint32_t b=avail&-avail; avail^=b; pos[r]=__builtin_ctz(b);
        go(r+1, cols|b, ((ld|b)<<1)&all, (rd|b)>>1, mirror); }
}
int main(int argc,char**argv){ n=atoi(argv[1]); uint32_t all=(1u<<n)-1;
    for(int c=0;c<n/2;c++){ uint32_t b=1u<<c; pos[0]=c; go(1,b,(b<<1)&all,b>>1,1); }
    if(n%2){ int c=n/2; uint32_t b=1u<<c; pos[0]=c; go(1,b,(b<<1)&all,b>>1,0); }
    uint64_t Q=0; for(int j=0;j<n;j++) for(int t=0;t<n;t++) Q+=K[0][j][t];
    printf("%d %llu\n",n,(unsigned long long)Q);
    for(int i=0;i<n;i++) for(int j=0;j<n;j++){ for(int t=0;t<n;t++) printf("%llu ",(unsigned long long)K[i][j][t]); printf("\n"); } }
