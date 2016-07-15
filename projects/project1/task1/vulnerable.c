#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/*
 * a vulnerable program
 */

long n = 0, c = 0, d = 0;

FILE *fp = NULL;

void say_hi()
{
  // loading data to array
  char line[5];
  printf("\nEnter your name fool:\n");
  gets(line);
  printf("\nHa! I have you now, %s\n", line);
}

int main()
{
    say_hi();
    return 0;
}
