__author__ = 'Davide'


class InputProvider:
    def get_heap_index(self, size):
        pass

    def get_val(self, index, cnt):
        pass


class ConsoleInputProvider(InputProvider):
    def _readInt(self, prompt, min_val, max_val):
        while True:
            val = int(input(prompt))
            if min_val <= val <= max_val:
                return val

    def get_val(self, index, cnt):
        return self._readInt("Amount to take from heap {}>".format(index),
                             1, cnt)

    def get_heap_index(self, size):
        return self._readInt("Choose heap [1-{}]>".format(size), 1, size)
