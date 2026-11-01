extern int piece_square[2][6][120];

int main(void)
{
    int side, kind, square;
    if (sizeof piece_square != 2880)
        return 1;
    for (side = 0; side < 2; ++side)
        for (kind = 0; kind < 6; ++kind)
            for (square = 0; square < 120; ++square)
                if (piece_square[side][kind][square] != 0)
                    return 2;
    piece_square[1][5][119] = 1234;
    if (piece_square[1][5][119] != 1234)
        return 3;
    return 0;
}
