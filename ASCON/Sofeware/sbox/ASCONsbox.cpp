#include <stdio.h>
#include "time.h"
#include <vcruntime_string.h>

int main() {
    //int ll, i;
    //for (ll = 0; ll <= 40; ll++) {
        //clock_t start = clock();
        //for (i = 0; i < 1000000; i++) {
            int x0, x1, x2, x3, x4, y0, y1, y2, y3, y4;
            x0 = 0x0000ffff;
            x1 = 0x00ff00ff;
            x2 = 0x0f0f0f0f;
            x3 = 0x33333333;
            x4 = 0x55555555;
            x0 ^= x4;
            x4 ^= x3;
            x2 ^= x1;
            y0 = x0;
            y4 = x4;
            y3 = x3;
            y1 = x1;
            y2 = x2;
            x0 = y0 ^ ((~y1) & y2);
            x2 = y2 ^ ((~y3) & y4);
            x4 = y4 ^ ((~y0) & y1);
            x1 = y1 ^ ((~y2) & y3);
            x3 = y3 ^ ((~y4) & y0);
            x1 ^= x0;
            x3 ^= x2;
            x0 ^= x4;
            x2 = ~x2;
        //}
        
        //sboxnew();

        //clock_t  stop = clock();
        //double duration = ((double)(stop - start)) / CLK_TCK;
        //printf("%d   time:%f\n", ll, duration);
    //}
    return 0;

}
