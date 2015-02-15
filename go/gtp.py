import sys
import go


def get_line():
    while True:
        line = sys.stdin.readline()
        if not line:
            return
        line = line.strip()
        hash_ = line.find('#')
        if hash_ != -1:
            line = line[:hash_]
        if line:
            yield line


def parse_command(line):
    words = line.split()
    if words[0].isdigit():
        id_ = words[0]
        command = words[1]
        args = words[2:]
    else:
        id_ = None
        command = words[0]
        args = words[1:]
    return id_, command, args


def write_success(id_, response):
    write = sys.stdout.write
    if id_ is not None:
        if response is not None:
            write('=%s %s\n\n' % (id_, response))
        else:
            write('=%s\n\n' % (id_,))
    else:
        if response is not None:
            write('= %s\n\n' % (response,))
        else:
            write('=\n\n')


def write_failure(id_, error):
    write = sys.stdout.write
    if id_ is not None:
        write('?%s %s\n\n' % (id_, error))
    else:
        write('? %s\n\n' % (error,))


def parse_vertex(vertex):
    vertex = vertex.lower()
    if vertex == 'pass':
        return
    letter = vertex[0]
    number = vertex[1:]
    row = go.SIZE - int(number)
    col = ord(letter) - ord('a')
    if col >= 8:
        col -= 1
    return row, col


def make_vertex(row, col):
    number = str(go.SIZE - row)
    if col >= 8:
        col += 1
    letter = chr(col + ord('a'))
    return letter + number


def parse_color(color):
    color = color.lower()
    color = color[0]
    if color == 'b':
        return go.BLACK
    else:
        return go.WHITE


def make_color(color):
    if color == 1:
        return 'black'
    else:
        return 'white'


class Basic:
    def __init__(self, commands):
        self.commands = commands

    def protocol_version(self):
        return '2'

    def known_command(self, command):
        if command in self.commands:
            return 'true'
        else:
            return 'false'

    def list_commands(self):
        return '\n'.join(self.commands)

    def quit(self):
        return


def list_commands(engine):
    members = dir(engine)
    commands = []
    for member in members:
        if not member.startswith('_'):
            commands.append(member)
    return commands


def get_response(obj, name, args):
    member = getattr(obj, name)
    if callable(member):
        return member(*args)
    else:
        return member


def get_error():
    info = sys.exc_info()
    if info[1] is None:
        return info[0]
    else:
        return str(info[1])


def run(engine):
    commands = list_commands(engine)
    basic = Basic(commands)
    quit_ = False
    for line in get_line():
        id_, command, args = parse_command(line)
        if command == 'quit':
            quit_ = True
        if hasattr(basic, command):
            response = get_response(basic, command, args)
            write_success(id_, response)
        elif hasattr(engine, command):
            try:
                response = get_response(engine, command, args)
                write_success(id_, response)
            except Exception:
                error = get_error()
                write_failure(id_, error)
        else:
            write_failure(id_, 'unknown command')
        sys.stdout.flush()
        if quit_:
            break
