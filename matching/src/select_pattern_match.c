/* REA5B00: select the current word pattern from the indexed table. */
extern int pattern,patterns[];
void select_pattern_5b00(int index)
{
    pattern=patterns[index];
}
