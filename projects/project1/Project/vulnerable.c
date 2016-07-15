#include <stdio.h>
#include <stdlib.h>

/*
 * a vulnerable program
 */

int main()
{
  char line[4];
  printf("\nEnter your name fool: ");
  gets(line);
  printf("\nHa! I have you now, %s\n", line);
  return 0;
}
