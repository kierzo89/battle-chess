/* Distinct real literal allocation and selector. */
char *select_beta(int active)
{
    if(active)return "beta ready";
    return "beta idle";
}
