#include <stdio.h>
#include "time.h"
//#include <vcruntime_string.h>
#define CRYPTO_KEYBYTES 16
#define CRYPTO_NSECBYTES 0
#define CRYPTO_NPUBBYTES 16
#define CRYPTO_ABYTES 16
#define CRYPTO_NOOVERLAP 1


#define U64BIG(x)                                                                  \
  ((((x) & 0x00000000000000FFULL) << 56) | (((x) & 0x000000000000FF00ULL) << 40) | \
   (((x) & 0x0000000000FF0000ULL) << 24) | (((x) & 0x00000000FF000000ULL) << 8) |  \
   (((x) & 0x000000FF00000000ULL) >> 8) | (((x) & 0x0000FF0000000000ULL) >> 24) |  \
   (((x) & 0x00FF000000000000ULL) >> 40) | (((x) & 0xFF00000000000000ULL) >> 56))


typedef unsigned char u8;
typedef unsigned long long u64;

typedef struct {
    u64 x0, x1, x2, x3, x4;
} state;

#define EXT_BYTE64(x, n) ((u8)((u64)(x) >> (8 * (7 - (n)))))
#define INS_BYTE64(x, n) ((u64)(x) << (8 * (7 - (n))))
#define ROTR64(x, n) (((x) >> (n)) | ((x) << (64 - (n))))

#define ROUND(C)                    \
  do {                              \
    state t;                        \
    s.x2 ^= C;                      \
    t.x0 = s.x3 ^ s.x4;             \
    t.x4 = s.x1 ^ s.x2;             \
    t.x3 = t.x0 | s.x0;             \
    t.x1 = t.x0 & s.x4;             \
    t.x3 ^= t.x4;                   \
    t.x2 = (~t.x4) ^ t.x1;          \
    t.x1 = t.x4 | s.x3;             \
    t.x4 &= s.x2;                   \
    t.x4 ^= s.x0;                   \
    t.x1 ^= s.x2;                   \
    t.x4 ^= s.x4;                   \
    t.x1 ^= t.x4;                   \
    t.x0 ^= (t.x4 | s.x1);          \
    t.x4 ^= t.x0;                   \
    s.x1 = t.x1;                    \
    s.x1 = ROTR64(s.x1, 39);        \
    s.x2 = t.x2;                    \
    s.x2 = ROTR64(s.x2, 1);         \
    s.x4 = t.x4;                    \
    t.x2 ^= s.x2;                   \
    s.x2 = ROTR64(s.x2, 6 - 1);     \
    s.x3 = t.x3;                    \
    t.x1 ^= s.x1;                   \
    s.x3 = ROTR64(s.x3, 10);        \
    s.x4 = ROTR64(s.x4, 7);         \
    t.x3 ^= s.x3;                   \
    s.x2 ^= t.x2;                   \
    s.x1 = ROTR64(s.x1, 61 - 39);   \
    s.x0 = t.x0;                    \
    s.x3 = ROTR64(s.x3, 17 - 10);   \
    t.x4 ^= s.x4;                   \
    s.x4 = ROTR64(s.x4, 41 - 7);    \
    s.x3 ^= t.x3;                   \
    s.x1 ^= t.x1;                   \
    s.x0 = ROTR64(s.x0, 19);        \
    s.x4 ^= t.x4;                   \
    t.x0 ^= s.x0;                   \
    s.x0 = ROTR64(s.x0, 28 - 19);   \
    s.x0 ^= t.x0;                   \
  } while (0)

#define P12()    \
  do {           \
    ROUND(0xf0); \
    ROUND(0xe1); \
    ROUND(0xd2); \
    ROUND(0xc3); \
    ROUND(0xb4); \
    ROUND(0xa5); \
    ROUND(0x96); \
    ROUND(0x87); \
    ROUND(0x78); \
    ROUND(0x69); \
    ROUND(0x5a); \
    ROUND(0x4b); \
  } while (0)

#define P8()     \
  do {           \
    ROUND(0xb4); \
    ROUND(0xa5); \
    ROUND(0x96); \
    ROUND(0x87); \
    ROUND(0x78); \
    ROUND(0x69); \
    ROUND(0x5a); \
    ROUND(0x4b); \
  } while (0)

#define P6()     \
  do {           \
    ROUND(0x96); \
    ROUND(0x87); \
    ROUND(0x78); \
    ROUND(0x69); \
    ROUND(0x5a); \
    ROUND(0x4b); \
  } while (0)




#define RATE (64 / 8)
#define PA_ROUNDS 12
#define PB_ROUNDS 6
#define IV                                                        \
  ((u64)(8 * (CRYPTO_KEYBYTES)) << 56 | (u64)(8 * (RATE)) << 48 | \
   (u64)(PA_ROUNDS) << 40 | (u64)(PB_ROUNDS) << 32)

int crypto_aead_encrypt(unsigned char* c, unsigned long long* clen,
    const unsigned char* m, unsigned long long mlen,
    const unsigned char* ad, unsigned long long adlen,
    const unsigned char* nsec, const unsigned char* npub,
    const unsigned char* k, unsigned long long* c1) {
    const u64 K0 = U64BIG(*(u64*)k);
    const u64 K1 = U64BIG(*(u64*)(k + 8));
    const u64 N0 = U64BIG(*(u64*)npub);
    const u64 N1 = U64BIG(*(u64*)(npub + 8));
    state s;
    u64 i;
    (void)nsec;

    // set ciphertext size
    *clen = mlen + CRYPTO_ABYTES;

    // initialization
    s.x0 = IV;
    s.x1 = K0;
    s.x2 = K1;
    s.x3 = N0;
    s.x4 = N1;
    P12();
    s.x3 ^= K0;
    s.x4 ^= K1;

    // process associated data
    unsigned long long adlenl = adlen;
    if (adlen) {
        while (adlen >= RATE) {
            s.x0 ^= U64BIG(*(u64*)ad);
            P6();
            adlen -= RATE;
            ad += RATE;
        }
        for (i = 0; i < adlenl; ++i, ++ad) s.x0 ^= INS_BYTE64(*ad, i);
        s.x0 ^= INS_BYTE64(0x80, adlen);
        P6();
    }
    s.x4 ^= 1;

    // process plaintext
    unsigned long long mlenl = mlen;
    while (mlen >= RATE) {
        s.x0 ^= U64BIG(*(u64*)m);
        *(u64*)c = U64BIG(s.x0);
        P6();
        mlen -= RATE;
        m += RATE;
        c += RATE;
    }

    for (i = 0; i < mlenl; ++i, ++m, ++c) {
        s.x0 ^= INS_BYTE64(*m, i);
        *c = EXT_BYTE64(s.x0, i);
    }
    s.x0 ^= INS_BYTE64(0x80, mlen);

    // finalization
    s.x1 ^= K0;
    s.x2 ^= K1;
    P12();
    s.x3 ^= K0;
    s.x4 ^= K1;

    // set tag
    *(u64*)c1 = U64BIG(s.x3);
    *(u64*)(c1 + 8) = U64BIG(s.x4);

    return 0;
}

int main() {
    unsigned char c[16];
    unsigned char m[8] = { 1,2,3,4,5,6,7,8 };
    const unsigned char ad[16] = { 1,2,3,4,5,6,7,8 , 1,2,3,4,5,6,7,8 };
    const unsigned char nsec[16] = { 1,2,3,4,5,6,7,8 , 1,2,3,4,5,6,7,8 };
    const unsigned char k[16] = { 1,2,3,4,5,6,7,8 , 1,2,3,4,5,6,7,8 };
    const unsigned char npub[16] = { 1,2,3,4,5,6,7,8 , 1,2,3,4,5,6,7,8 };
   // int ll = 8;
    //for (ll = 8; ll <= 2048; ll = 2 * ll) {
        //memset(m, 0, 8);

        u64 clen[5] = { 0,0,0,0,0 };
        u64 mlen = 8, adlen = 0;
        u64 c1[2];
        int i;
        //clock_t start = clock();
        //for (i = 0; i < 1000000; i++) {
            crypto_aead_encrypt(c, clen, m, mlen, ad, adlen, nsec, npub, k, c1);
        //}
        //sbox();
        //sboxnew();

        //clock_t  stop = clock();
        //double duration = ((double)(stop - start)) / CLK_TCK;
        //printf("%d byte time:%f\n", ll, duration);
   // }
    return 0;

}
