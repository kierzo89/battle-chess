/* REA image 7DA8: reconstruct the eight-byte state as four 16-bit words.
 * Original field names are unknown. Placements are linker configuration.
 */
typedef union {unsigned word;struct{unsigned char kind,capture;} bytes;} MoveKind;
typedef struct {int to,from,flag;MoveKind detail;} Move;

extern int counter;
extern Move current_state;
extern Move initial_move;

void init_state(void)
{
    counter = -1;
    current_state = initial_move;
}
