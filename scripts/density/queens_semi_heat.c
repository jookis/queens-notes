/* Heatmap of all placements with one queen per row and column plus diagonal rules.
   mode 2: both diagonal families (ordinary queens). mode 1: only the down-right family (c - r constant). */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
static int n, mode; static uint64_t heat[32][32], total; static int pos[32];
static void go(int r, uint32_t cols, uint64_t dr, uint64_t dl){
    if(r==n){ total++; for(int i=0;i<n;i++) heat[i][pos[i]]++; return; }
    for(int c=0;c<n;c++){
        if(cols>>c&1) continue;
        int a=c-r+n-1, b=c+r;
        if(dr>>a&1) continue;
        if(mode==2 && (dl>>b&1)) continue;
        pos[r]=c; go(r+1, cols|1u<<c, dr|1ull<<a, dl|1ull<<b);
    }
}
int main(int argc,char**argv){ n=atoi(argv[1]); mode=atoi(argv[2]); go(0,0,0,0);
    printf("%d %d %llu\n",n,mode,(unsigned long long)total);
    for(int i=0;i<n;i++){ for(int j=0;j<n;j++) printf("%llu ",(unsigned long long)heat[i][j]); printf("\n"); } }
