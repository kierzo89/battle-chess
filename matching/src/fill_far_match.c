/* REA5A4F: fill bytes through a huge pointer, preserving segment carry. */
void fill_5a4f(char huge *destination,int count,char value)
{
    for (;count;count--) *destination++=value;
}
