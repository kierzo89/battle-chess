/* Diagnostic separate translation units deliberately share one PUBLIC CODE name. */
extern int far translation_target(int);
int far translation_caller(int value)
{
    return translation_target(value)+3;
}
