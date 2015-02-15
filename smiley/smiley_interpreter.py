__author__ = 'davide'

import sys
import numpy as np

CODES = [":)", ":(", ":P", ":O", ":S", ":D", ":[", ":]", ":+", ":-",
         ":*", ":/", "^_^", "O_O", "U_U", "*_*", ":<", ":>", ":&",
         ":|", ":~", ":X"]

[RIGHT, LEFT, INCR, DECR, INPUT, OUTPUT, WHILE, WEND, ADD, SUB, MUL, DIV, XCHG,
 DUP, ZERO, ONES, SHL, SHR, AND, OR, NOT, XOR] = CODES


def pprint(code):
    indent_level = 0
    line = True
    for instruction in code:
        if isinstance(instruction, tuple):
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
            print(instruction, end=" ")
        if instruction == WHILE:
            indent_level += 4


def assemble(code):
    """
    Assemble the code
    @param code: list of opcodes
    @type code: str
    @return: a list of codes
    """
    assembled = []
    last_opened = []
    ip = 0
    for opcode in code.split():
        if opcode not in CODES:
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

    def incr_mp(mp):
        return (mp + 1) % mem_size

    def decr_mp(mp):
        return (mp + mem_size - 1) % mem_size

    while ip < len(code):
        instr = code[ip]
        if instr == LEFT:
            mp = decr_mp(mp)
        elif instr == RIGHT:
            mp = incr_mp(mp)
        elif instr == INCR:
            memory[mp] += 1
        elif instr == DECR:
            memory[mp] -= 1
        elif instr == INPUT:
            input_str = in_file.readline().strip() or "\0"
            assert isinstance(input_str, str)
            memory[mp] = ord(input_str[0])
        elif instr == OUTPUT:
            out_file.write(chr(memory[mp]))
            if hasattr(out_file, "flush"):
                out_file.flush()
        elif instr == ADD:
            memory[mp] += memory[incr_mp(mp)]
        elif instr == SUB:
            memory[mp] -= memory[incr_mp(mp)]
        elif instr == MUL:
            memory[mp] *= memory[incr_mp(mp)]
        elif instr == DIV:
            memory[mp] /= memory[incr_mp(mp)]
        elif instr == XCHG:
            imp = incr_mp(mp)
            memory[mp], memory[imp] = memory[imp], memory[mp]
        elif instr == DUP:
            memory[incr_mp(mp)] = memory[mp]
        elif instr == ZERO:
            memory[mp] = 0
        elif instr == ONES:
            memory[mp] = 0xFF
        elif instr == SHL:
            memory[mp] <<= 1
        elif instr == SHR:
            memory[mp] >>= 1
        elif instr == AND:
            memory[mp] &= memory[incr_mp(mp)]
        elif instr == OR:
            memory[mp] |= memory[incr_mp(mp)]
        elif instr == NOT:
            memory[mp] = ~memory[mp]
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
            print("Instruction", instr)
            print("IP: {}".format(ip))
            print("MP: {}".format(mp))
            print("MEM: {}".format(memory))


if __name__ == "__main__":
    code = []
    filepath = "all.sm"
    with open(filepath) as input_file:
        for line in input_file:
            if line[0] != "#":
                code.append("".join(line.strip()))
    code = " ".join(code)
    if code:
        assembled = assemble(code)
        print("Code:")
        pprint(assembled)
        print()
        print("Running...")
        run(assembled)
