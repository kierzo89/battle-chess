/* Signed screen-coordinate hit test: eight rows, cancel, optional action. */
int dialog_hit_d840(int x,int y,int allow_extra)
{
 if(x>60 && x<187 && y>60 && y<139)return (y-60)/10;
 if(x>200 && x<253 && y>129 && y<141)return 8;
 if(allow_extra && x>200 && x<253 && y>109 && y<121)return 9;
 return 255;
}
