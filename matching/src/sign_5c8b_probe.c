/* Complete three-way signed return including compiler-emitted dead jumps. */
int sign_5c8b(int value)
{
 if(value>0)return 1;
 else if(value<0)return -1;
 else return 0;
}
