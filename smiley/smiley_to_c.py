from functools import partial
import itertools as it

from smiley.smiley_interpreter import RIGHT, LEFT, INCR, DECR, INPUT, \
    OUTPUT, WHILE, WEND, ADD, SUB, MUL, DIV, XCHG, DUP, ZERO, ONES, SHL, SHR, \
    AND, OR, NOT, XOR, assemble, pprint


def to_c_code(code, out_file, mem_size=3e4):
    mem_size = int(mem_size)
    p_to_f = partial(print, file=out_file)

    def aggr(code):
        for v, g in it.groupby(code):
            yield v, len(list(g))

    p_to_f("#include <stdio.h>\n")
    p_to_f("#define MEM_SIZE {}\n".format(mem_size))
    p_to_f(
        "inline char* incr(char* mp, char* mem, char* end, int a){ mp+=a;if("
        "mp >= "
        "end) mp = mem + (end - mp); return mp; }")
    p_to_f(
        "inline char* decr(char* mp, char* mem, char* end, int a){ mp-=a;if("
        "mp < "
        "mem) "
        "mp = end - (mem - mp); return mp; }")
    p_to_f("int main(void){")
    p_to_f("char mem[MEM_SIZE]; register char* mem_ptr = mem;")
    p_to_f("register char* end = mem + MEM_SIZE;")
    p_to_f("char tmp = 0;")

    for instruction, num in aggr(code):
        if instruction == LEFT:
            p_to_f("mem_ptr = decr(mem_ptr, mem, end, {});".format(num))
        elif instruction == RIGHT:
            p_to_f("mem_ptr = incr(mem_ptr, mem, end, {});".format(num))
        elif instruction == INCR:
            p_to_f("*mem_ptr += {};".format(num))
        elif instruction == DECR:
            p_to_f("*mem_ptr -= {};".format(num))
        elif instruction == INPUT:
            p_to_f("*mem_ptr = getchar();\n" * num)
        elif instruction == OUTPUT:
            p_to_f("putchar(*mem_ptr);\n" * num)
        elif instruction == WHILE:
            p_to_f("while(*mem_ptr){\n" * num)
        elif instruction == WEND:
            p_to_f("}\n" * num)
        elif instruction == ADD:
            p_to_f("*mem_ptr += *(incr(mem_ptr, mem, end, 1));\n" * num)
        elif instruction == SUB:
            p_to_f("*mem_ptr -= *(incr(mem_ptr, mem, end, 1));\n" * num)
        elif instruction == MUL:
            p_to_f("*mem_ptr *= *(incr(mem_ptr, mem, end, 1));\n" * num)
        elif instruction == DIV:
            p_to_f("*mem_ptr /= *(incr(mem_ptr, mem, end, 1));\n" * num)
        elif instruction == XCHG:
            p_to_f(
                "tmp = *mem_ptr; *mem_ptr = *(incr(mem_ptr, mem, end, 1)); *("
                "incr("
                "mem_ptr, mem, end, 1)) = tmp;\n" * num)
        elif instruction == DUP:
            p_to_f("*(incr(mem_ptr, mem, end, 1)) = *mem_ptr;\n" * num)
        elif instruction == ZERO:
            p_to_f("*mem_ptr = 0;")
        elif instruction == ONES:
            p_to_f("*mem_ptr = 0xFF;")
        elif instruction == SHL:
            p_to_f("*mem_ptr <<= {};".format(num))
        elif instruction == SHR:
            p_to_f("*mem_ptr >>= {};".format(num))
        elif instruction == AND:
            p_to_f("*mem_ptr &= *(incr(mem_ptr, mem, end, 1));\n" * num)
        elif instruction == OR:
            p_to_f("*mem_ptr |= *(incr(mem_ptr, mem, end, 1));\n" * num)
        elif instruction == NOT:
            p_to_f("*mem_ptr = ~*mem_ptr;\n" * num)
        elif instruction == XOR:
            p_to_f("*mem_ptr ^= *(incr(mem_ptr, mem, end, 1));\n" * num)

    p_to_f("}")


if __name__ == "__main__":
    code = []
    filepath = "somma.sm"
    with open(filepath) as input_file:
        for line in input_file:
            if line[0] != "#":
                code.append("".join(line.strip()))
    code = " ".join(code)
    if code:
        assembled = assemble(code)
        print("Code:")
        pprint(assembled)

        with open("dst.c", "w") as out:
            to_c_code(assembled, out)