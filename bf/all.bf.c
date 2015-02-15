#include <stdio.h>

#define MEM_SIZE 30000

int main(void)
{
    char mem[MEM_SIZE];
    register char* mem_ptr = mem;
    register char* end = mem + MEM_SIZE;
    putchar(*mem_ptr);

    *mem_ptr += 1;
    while(*mem_ptr)
    {
        putchar(*mem_ptr);
        *mem_ptr += 1;
    }
}
