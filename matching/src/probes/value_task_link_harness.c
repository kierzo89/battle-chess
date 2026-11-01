/* Synthetic fixture definitions; no original allocation ownership claim. */
typedef struct AnimationTask { unsigned char fixture[24]; } AnimationTask;
extern int value_index,task_index;
extern char value_return_message[],exhausted_message[];
extern char task_return_message[],task_exhausted_message[];
extern void push_value(int),release_task_3ae3(AnimationTask *);
extern int pop_value(void);
extern AnimationTask *allocate_task_3b0c(void);
extern int values[4];
extern AnimationTask *task_pool[4];
static AnimationTask fixture_tasks[4];
static int errors;
static char *last_error;
int error_message(char *message)
{
    errors++;last_error=message;return 77;
}
int main(void)
{
    int i;
    AnimationTask *p;
    if(value_index || task_index)return 1;
    for(i=0;i<4;i++)if(values[i] || task_pool[i])return 10;
    for(i=0;i<4;i++) {values[i]=11*(i+1);task_pool[i]=&fixture_tasks[i];}
    push_value(99);
    if(value_index || errors!=1 || last_error!=value_return_message)return 2;
    release_task_3ae3(&fixture_tasks[0]);
    if(task_index || errors!=2 || last_error!=task_return_message)return 3;
    for(i=0;i<4;i++)if(pop_value()!=11*(i+1))return 4;
    if(value_index!=4 || pop_value()!=77 || errors!=3 || last_error!=exhausted_message)return 5;
    push_value(99);
    if(value_index!=3 || pop_value()!=99 || value_index!=4)return 6;
    for(i=0;i<4;i++)if(allocate_task_3b0c()!=&fixture_tasks[i])return 7;
    if(task_index!=4 || allocate_task_3b0c()!=(AnimationTask *)77 || errors!=4 || last_error!=task_exhausted_message)return 8;
    p=&fixture_tasks[1];release_task_3ae3(p);
    if(task_index!=3 || allocate_task_3b0c()!=p || task_index!=4)return 9;
    return 0;
}
