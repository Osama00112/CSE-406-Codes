/* This program has a buffer overflow vulnerability. */
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

int foo(char *str)
{
        char buffer[101];
        /* The following statement has a buffer overflow problem */
        strcpy(buffer, str);
        return 2;
}

int main(int argc, char **argv)
{
        char str[401];
        FILE *badfile;
        badfile = fopen("badfile", "r");
        fread(str, sizeof(char), 401, badfile);
        foo(str);

        printf("Returned Properly\n");
        return 2;
}
