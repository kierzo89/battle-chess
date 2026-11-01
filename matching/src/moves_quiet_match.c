/* REA 9BBC. Complete65-byte MSC5.00 /AS /Zi match. */
typedef struct {int from,to,flag; unsigned char kind,capture;} Move;
int quiet_9bbc(p) Move *p;
{
    int result;
    result=(p->kind!=0) & (p->kind!=6) & (p->capture==0) & (p->flag==0);
    return result;
}
