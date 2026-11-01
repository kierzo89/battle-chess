/* 3B0C: allocate one of four preassigned near task records. */
typedef struct AnimationTask AnimationTask;
extern int task_index;
extern AnimationTask *task_pool[4];
extern int error_message(char *);
extern char task_exhausted_message[];
AnimationTask *allocate_task_3b0c(void)
{
 if(task_index<4)return task_pool[task_index++];
 return (AnimationTask *)error_message(task_exhausted_message);
}
