/* Count every n-queens solution by (top-row column, bottom-row column). Bitmask backtracking. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
static int n; static uint64_t J[32][32]; static int top;
static void go(int r, uint32_t cols, uint32_t ld, uint32_t rd){
    uint32_t all=(1u<<n)-1, avail=all&~(cols|ld|rd);
    if(r==n-1){ while(avail){ uint32_t b=avail&-avail; avail^=b; J[top][__builtin_ctz(b)]++; } return; }
    while(avail){ uint32_t b=avail&-avail; avail^=b; if(r==0) top=__builtin_ctz(b);
        go(r+1, cols|b, ((ld|b)<<1)&all, (rd|b)>>1); }
}
int main(int argc,char**argv){ n=atoi(argv[1]); go(0,0,0,0);
    uint64_t t=0; for(int i=0;i<n;i++) for(int j=0;j<n;j++) t+=J[i][j];
    printf("%d %llu\n",n,(unsigned long long)t);
    for(int i=0;i<n;i++){ for(int j=0;j<n;j++) printf("%llu ",(unsigned long long)J[i][j]); printf("\n"); } }
