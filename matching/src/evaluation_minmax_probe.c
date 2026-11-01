/* Candidate source only: disjoint REA bodies still require extent proof. */
int far evaluation_max(register int left, register int right)
{
    if (left >= right) return left;
    else return right;
}

int far evaluation_min(register int left, register int right)
{
    if (left <= right) return left;
    else return right;
}
