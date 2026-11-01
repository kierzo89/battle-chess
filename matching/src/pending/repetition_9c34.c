/* Eight-byte history records used by the repetition detector. */
typedef struct { int from, to, other0, other1; } Pair;
extern Pair pairs[];
extern int counter_9880;
extern int quiet_9bbc(Pair *);
extern int lowbit_a514(int);
int repetition_9c34(int required)
{
    int a,b,c,d,e,f,g,h,i;
    a = 1;
    g = 1;
    h = counter_9880 + 1;
    f = h - 4;
    i = h;
    while (quiet_9bbc(&pairs[i]-1) & ((f < i) | !required)) i--;
    if (f < i) return a;
    d = h;
    for (;;) {
        d--;
        b = pairs[d].from;
        e = d + 2;
        while (e < h) {
            if (pairs[e].to == b) goto next;
            e += 2;
        }
        e = d;
        c = pairs[e].to;
        do {
            if (e - 2 < i) return a;
            e -= 2;
            if (pairs[e].from == c) c = pairs[e].to;
        } while (!((c == b) & (f + 1 >= e)));
        if (e < f) {
            f = e;
            if (lowbit_a514(h-f)) {
                if (f == i) return a;
                f--;
            }
            d = h;
        }
next:
        if (d <= f) {
            g++;
            a = g;
            if (f - 2 < i) return a;
            h = f;
            f -= 2;
            d = h;
        }
    }
    return a;
}
