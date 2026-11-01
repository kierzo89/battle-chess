/* Four genuine adjacent value/task pool operations, image3A99..3B2C. */
typedef struct AnimationTask AnimationTask;
extern int value_index,values[4];
extern int task_index;
extern AnimationTask *task_pool[4];
extern int error_message(char *);
extern char value_return_message[],exhausted_message[];
extern char task_return_message[],task_exhausted_message[];
void push_value(int value)
{
 if(value_index){values[--value_index]=value;return;}
 error_message(value_return_message);
}
int pop_value(void)
{
 if(value_index<4)return values[value_index++];
 return error_message(exhausted_message);
}
void release_task_3ae3(AnimationTask *task)
{
 if(task_index){task_pool[--task_index]=task;return;}
 error_message(task_return_message);
}
AnimationTask *allocate_task_3b0c(void)
{
 if(task_index<4)return task_pool[task_index++];
 return (AnimationTask *)error_message(task_exhausted_message);
}
