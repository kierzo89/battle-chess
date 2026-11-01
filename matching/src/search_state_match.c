/* MSC 5.00 /AS /Gs /Os matches; MSC 5.10 emits one extra internal NOP.
   Address names describe observed storage, not recovered original symbols. */
typedef union {
    int word;
    struct { char low; char high; } bytes;
} StateWord;

typedef struct {
    int word0;
    int word1;
    int word2;
    StateWord word3;
} SearchState;

extern int counter_9880;
extern SearchState state_8d12;
extern void generate_a348(void);
extern void advance_a4d4(void);
extern int predicate_86d6(int, int, int, int);

int search_state_8fca(void)
{
    counter_9880++;
    generate_a348();
    counter_9880--;
    advance_a4d4();
    if (!state_8d12.word3.bytes.low)
        goto exhausted;
repeat:
    if (!predicate_86d6(state_8d12.word0, state_8d12.word1,
                        state_8d12.word2, state_8d12.word3.word))
        return 1;
    advance_a4d4();
    if (state_8d12.word3.bytes.low)
        goto repeat;
exhausted:
    return 0;
}
