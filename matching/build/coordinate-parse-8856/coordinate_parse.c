/* Convert algebraic file/rank characters to the engine's 0x88 square.
 * The native invalid-input path returns an uninitialized automatic word.
 * Preserve that observed limitation; do not invent a default/error sentinel. */
extern int tolower(int);
int parse_square_8856(char file,char rank)
{
    int square;
    file=tolower(file);
    if(file>='a'&&file<='h'&&rank>='1'&&rank<='8')
        square=rank*16+file-0x371;
    return square;
}
