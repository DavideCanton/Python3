from collections import namedtuple, deque
from fractions import Fraction

Node = namedtuple("Node", "range value")


def get_t(point_list):
    x_list = [x[0] for x in point_list]
    val_queue = deque([Node(range=(i, i),
                            value=Fraction(x[1]).limit_denominator())
                       for i, x in enumerate(point_list)])
    temp_queue = deque()
    res_list = []
    while len(res_list) < len(point_list):
        res_list.append(val_queue[0].value)
        while len(val_queue) > 1:
            p = val_queue.popleft()
            p1 = val_queue[0]
            range_ = (p.range[0], p1.range[1])
            value = Fraction((p.value - p1.value) /
                             (x_list[p.range[0]] - x_list[p1.range[1]]))
            value = value.limit_denominator()
            temp_queue.append(Node(range=range_, value=value))
        val_queue.clear()
        val_queue.extend(temp_queue)
        temp_queue.clear()
    return res_list


l = [(0, 0), (0.5, 3), (1, 1)]
print(l)
print(get_t(l))
