__author__ = 'davide'

import sys
import numpy as np
from pathlib import Path
from functools import partial
import itertools as it

codes = '<>+-,.[]'

LEFT, RIGHT, INCR, DECR, INPUT, OUTPUT, WHILE, WEND = list(codes)


def to_c_code(code, out_file, mem_size=3e4):
    mem_size = int(mem_size)
    p_to_f = partial(print, file=out_file)

    def aggr(code):
        for v, g in it.groupby(code):
            yield v, len(list(g))

    p_to_f("#include <stdio.h>\n")
    p_to_f("#define MEM_SIZE {}\n".format(mem_size))
    p_to_f("int main(void){")
    p_to_f("char mem[MEM_SIZE]; register char* mem_ptr = mem;")
    p_to_f("register char* end = mem + MEM_SIZE;")

    for instruction, num in aggr(code):
        if instruction == LEFT:
            p_to_f("mem_ptr -= {};".format(num))
            p_to_f("if(mem_ptr < mem) mem_ptr = end - (mem - mem_ptr);")
        elif instruction == RIGHT:
            p_to_f("mem_ptr += {};".format(num))
            p_to_f("if(mem_ptr >= end) mem_ptr = mem + (end - mem_ptr);")
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
    p_to_f("}")


def pprint(code):
    indent_level = 0
    line = True
    for instruction in code:
        if len(instruction) == 2:
            instruction, _ = instruction
            if instruction == WEND:
                indent_level -= 4
        instr_string = instruction
        if line:
            print(" " * indent_level, end="")
            line = False
        if instr_string in [WHILE, WEND]:
            print("\n{}\n".format(instruction), end="")
            line = True
        else:
            print(instruction, end="")
        if instruction == WHILE:
            indent_level += 4


def assemble(code):
    """
    Assemble the code
    @param code: list of opcodes
    @type code: list[int]
    @return: a list of codes
    """
    assembled = []
    last_opened = []
    ip = 0
    for opcode in code:
        if opcode not in codes:
            continue
        elif opcode == WHILE:
            last_opened.append(ip)
            assembled.append((WHILE, -1))
            ip += 1
        elif opcode == WEND:
            last = last_opened.pop()
            assembled[last] = WHILE, ip + 1
            assembled.append((WEND, last + 1))
            ip += 1
        else:
            assembled.append(opcode)
            ip += 1
    if last_opened:
        raise ValueError("Invalid code!")
    return assembled


def run(code, mem_size=3E4, debug=False,
        in_file=sys.stdin, out_file=sys.stdout):
    """
    Runs the code.
    @param code: the code.
    @type code: list[int]
    @param mem_size: mem size
    @type mem_size: float
    @param debug: debug
    @type debug: bool
    @param in_file: input file
    @type in_file: file
    @param out_file: output file
    @type out_file: file
    @return:
    """
    memory = np.zeros(mem_size, dtype=np.uint8)
    ip = 0
    mp = 0
    while ip < len(code):
        instr = code[ip]
        if instr == LEFT:
            mp = (mp + mem_size - 1) % mem_size
        elif instr == RIGHT:
            mp = (mp + 1) % mem_size
        elif instr == INCR:
            memory[mp] += 1
        elif instr == DECR:
            memory[mp] -= 1
        elif instr == INPUT:
            input_str = in_file.readline().strip() or "\0"
            memory[mp] = ord(input_str[0])
        elif instr == OUTPUT:
            out_file.write(chr(memory[mp]))
            out_file.flush()
        else:
            instr, jmp = instr
            if instr == WHILE:
                if not memory[mp]:
                    ip = jmp - 1
            elif instr == WEND:
                if memory[mp]:
                    ip = jmp - 1
        ip += 1
        if debug:
            print("IP: {}".format(ip))
            print("MP: {}".format(mp))
            print("MEM: {}".format(memory))


if __name__ == "__main__":
    code = []
    filepath = Path("all.bf")
    with filepath.open() as input_file:
        for line in input_file:
            code.append("".join(line.strip()))
    code = "".join(code)
    if code:
        assembled = assemble(code)
        print("Code:")
        pprint(assembled)
        print()
        print("Running...")
        run(assembled)

    with open(str(filepath) + ".c", "w") as f:
        to_c_code(code, f)
