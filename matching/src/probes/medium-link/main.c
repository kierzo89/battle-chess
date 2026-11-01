/* Small-model startup/main ABI with actual initialized shared storage. */
int shared_state = 3;
extern int far medium_a(int);
int main(void)
{
    return medium_a(7) != ((7 ^ 0x1357) + 6);
}
