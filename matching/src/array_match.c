/* REA image 3AC2. Signed cursor, four-word array, caller-cleanup error call.
 * The error routine's external behavior remains unresolved.
 */
extern int value_index;
extern int values[4];
extern int error_message(char *);
extern char exhausted_message[];

int pop_value(void)
{
    if (value_index < 4)
        return values[value_index++];
    return error_message(exhausted_message);
}
