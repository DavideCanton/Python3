#include <stdio.h>

#define MEM_SIZE 30000

inline char* incr(char* mp, char* mem, char* end, int a){ mp+=a;if(mp >= end) mp = mem + (end - mp); return mp; }
inline char* decr(char* mp, char* mem, char* end, int a){ mp-=a;if(mp < mem) mp = end - (mem - mp); return mp; }
int main(void){
char mem[MEM_SIZE]; register char* mem_ptr = mem;
register char* end = mem + MEM_SIZE;
char tmp = 0;
*mem_ptr = getchar();

mem_ptr = incr(mem_ptr, mem, end, 1);
*mem_ptr += 1;
*mem_ptr <<= 5;
mem_ptr = incr(mem_ptr, mem, end, 1);
*mem_ptr += 1;
*mem_ptr <<= 4;
mem_ptr = decr(mem_ptr, mem, end, 1);
*mem_ptr += *(incr(mem_ptr, mem, end, 1));

mem_ptr = decr(mem_ptr, mem, end, 1);
*mem_ptr -= *(incr(mem_ptr, mem, end, 1));

mem_ptr = incr(mem_ptr, mem, end, 1);
*mem_ptr = getchar();

mem_ptr = decr(mem_ptr, mem, end, 1);
*mem_ptr += *(incr(mem_ptr, mem, end, 1));

putchar(*mem_ptr);

mem_ptr = incr(mem_ptr, mem, end, 1);
*mem_ptr = 0;
*mem_ptr += 1;
*mem_ptr <<= 3;
*mem_ptr += 2;
putchar(*mem_ptr);

}
