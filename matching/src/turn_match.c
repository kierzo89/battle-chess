/* REA 7DDB. C5.00 /AS /Gs /Os emits all144 original bytes.
 * Address names describe observed storage and calls, not original symbols.
 */
typedef struct {
    unsigned char square;
    char remaining[31];
} SideInfo;

extern int state_cbd2;
extern int state_934c;
extern int search_state_8fca(void);
extern void no_move(void);
extern int side_9846;
extern int side_a836;
extern SideInfo side_info_9604[];
extern int attacked_9a50(int, int);
extern char check_8f44;
extern int waiting_0eee;
extern void far draw_fce8(int);
extern void poll_8aaa(void);
extern int ready_9856;
extern int obtain_input(void);
extern void step_872a(void);
extern int input_083e(void);
extern void dispatch_8d73(int);
extern int state_57cc;

void turn_7ddb(void)
{
    int result;
    state_cbd2 = 0;
    state_934c = 0;
    if (!search_state_8fca()) {
        no_move();
    } else {
        check_8f44 = attacked_9a50(side_a836, side_info_9604[side_9846].square);
        waiting_0eee = 1;
        draw_fce8(side_9846);
        do {
            poll_8aaa();
            if (!ready_9856)
                ready_9856 = obtain_input();
            if (ready_9856)
                step_872a();
            result = input_083e();
            if (result) {
                dispatch_8d73(result);
                return;
            }
        } while (!ready_9856);
        waiting_0eee = 0;
        state_57cc = 1;
    }
}
