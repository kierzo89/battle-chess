/* Genuine far call with a forward-defined target in one medium-model source. */
int far translation_target(int);
int far translation_caller(int value)
{
    return translation_target(value)+3;
}
int far translation_target(int value)
{
    return (value*3)^0x25;
}
