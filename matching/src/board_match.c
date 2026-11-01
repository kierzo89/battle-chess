/* REA 7DBF: assign two bytes in a four-byte board cell.
 * The remaining bytes and original field names are not established here.
 */
typedef struct {
    char first;
    char second;
    char remaining[2];
} Cell;

extern Cell board[];

void set_cell_bytes(char first, char second, int square)
{
    board[square].first = first;
    board[square].second = second;
}
