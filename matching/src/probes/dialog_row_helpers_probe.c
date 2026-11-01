int next_dialog_row_db3d(char rows[8][16],int row)
{
 do {
  ++row;
  if(row>=8)row=0;
 }while(rows[row][15]==-1);
 return row;
}
int previous_dialog_row_db65(char rows[8][16],int row)
{
 do {
  --row;
  if(row<0)row=7;
 }while(rows[row][15]==-1);
 return row;
}
