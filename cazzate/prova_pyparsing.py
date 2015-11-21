from pyparsing import *

plus_or_minus = oneOf("+ -")
mul_or_div = oneOf("* /")

unsigned_int = Word(nums)
opt_signed_int = Optional(plus_or_minus) + unsigned_int
point = "."
float_num = Combine(Optional(plus_or_minus) +
                    ((unsigned_int + point + Optional(unsigned_int)) | (point + unsigned_int))
                    + Optional(CaselessLiteral("e") + opt_signed_int))

moodle_var = Suppress("{") + Word(alphas, alphanums) + Suppress("}")
# here I use the ^ operator to match the longest grammar.
real_num = (float_num ^ opt_signed_int ^ "pi()" ^ moodle_var)

mul_op = Forward()
expr = Forward()
add_op = mul_op + ZeroOrMore(plus_or_minus + mul_op)
mul_op << expr + ZeroOrMore(mul_or_div + expr)
function = Word(alphas, alphanums) + Suppress("(") + add_op + Suppress(")")
expr << ((Suppress("(") + add_op + Suppress(")")) ^ real_num ^ function)

print(float_num.parseString("2.1e+12"))
