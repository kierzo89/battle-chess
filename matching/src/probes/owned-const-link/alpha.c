/* Target-free literal-return control; no original game storage. */
char *select_alpha(int active)
{
    if(active)return "alpha ready";
    return "alpha idle";
}
