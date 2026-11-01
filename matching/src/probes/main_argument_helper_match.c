/* Prefix comparison used for command-line option names.  Returns the first
 * unmatched byte of expected, or zero once expected is exhausted. */
extern int tolower(int);
int compare_argument(register char *argument,register char *expected)
{
 while(tolower(*argument)==tolower(*expected) && *expected) {
  argument++;expected++;
 }
 return *expected;
}
