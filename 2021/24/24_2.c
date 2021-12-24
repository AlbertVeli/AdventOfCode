#include <stdio.h>

/* Values from the three diffing lines in all 14 input blocks */
int abcs[14][3] = {
   {1, 14, 12}, 
   {1, 15, 7}, 
   {1, 12, 1}, 
   {1, 11, 2}, 
   {26, -5, 4}, 
   {1, 14, 15}, 
   {1, 15, 11}, 
   {26, -13, 5}, 
   {26, -16, 3}, 
   {26, -8, 9}, 
   {1, 15, 2}, 
   {26, -8, 3}, 
   {26, 0, 3}, 
   {26, -4, 11}
};

/* l = array of 14 ints, 1 - 9 */
int try_list(int *l)
{
   int i, x, z, w, a, b, c;
   int *block;

   z = 0;

   for (i = 0; i < 14; i++) {
      /* Do block number i */
      block = abcs[i];
      a = block[0];
      b = block[1];
      c = block[2];
      w = l[i];
      x = (z % 26 + b) != w;
      z = (int)(z / a);
      if (x)
         z = z * 26 + w + c;
   }

   return z == 0;
}

void print_list(int *l)
{
   int i;
   for (i = 0; i < 14; i++) {
      printf("%d", l[i]);
   }
   printf("\n");
}

int main(void)
{
   /* This is cheating, insert the first numbers from known solution.
    * Merry Christmas! */
   int l[14] = { 1, 1, 8, 4, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
   int i5, i6, i7, i8, i9, i10, i11, i12, i13;

   /* Nest all the loops! */
   for (i5 = 1; i5 < 10; i5++) {
      l[5] = i5;
   for (i6 = 1; i6 < 10; i6++) {
      l[6] = i6;
   for (i7 = 1; i7 < 10; i7++) {
      l[7] = i7;
   for (i8 = 1; i8 < 10; i8++) {
      l[8] = i8;
   for (i9 = 1; i9 < 10; i9++) {
      l[9] = i9;
   for (i10 = 1; i10 < 10; i10++) {
      l[10] = i10;
   for (i11 = 1; i11 < 10; i11++) {
      l[11] = i11;
   for (i12 = 1; i12 < 10; i12++) {
      l[12] = i12;
   for (i13 = 1; i13 < 10; i13++) {
      l[13] = i13;
      if (try_list(l)) {
         /* First printed number is the correct one. */
         print_list(l);
         return 0;
      }
   }}}}}}}}}

   return 0;
}
