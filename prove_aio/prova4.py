import asyncio


@asyncio.coroutine
def compute_collatz_length(x):
    n = 0
    while x > 1:
        if x % 2 == 0:
            x //= 2
        else:
            x = 3 * x + 1
        n += 1
        yield
    return n


class CoroCtx:
    def __init__(self, fact, max_):
        self.cur = 0
        self.fact = fact
        self.max = max_
        self.buffer = {}

    @asyncio.coroutine
    def print_to_file(self, f, vals):
        for v in vals:
            val = yield from compute_collatz_length(v)
            self.buffer[v] = val

            if all(self.cur + i in self.buffer for i in range(self.fact)):
                for i in range(self.fact):
                    c = self.cur + i
                    print(c, "->", self.buffer[c], file=f)
                    del self.buffer[c]
                self.cur += self.fact


if __name__ == "__main__":
    MAX = 10000
    FACT = 500
    ctx = CoroCtx(FACT, MAX)

    loop = asyncio.get_event_loop()
    with open("prova.txt", "w") as f_out:
        task_list = [ctx.print_to_file(f_out, range(i, MAX, FACT))
                     for i in range(FACT)]
        loop.run_until_complete(asyncio.wait(task_list))
    loop.close()