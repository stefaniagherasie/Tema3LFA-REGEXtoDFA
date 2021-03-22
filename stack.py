from regex import Regex


class Stack:
    def __init__(self):
        self.stack = []

    def push(self, el):
        self.stack.append(el)

    def peek(self, pos):
        if pos < len(self.stack):
            return self.stack[-(pos + 1)]

        return None

    def pop(self):
        el = self.peek(0)
        self.stack.pop()
        return el

    def add(self, el):
        self.stack.insert(0, el)

    def empty(self):
        return self.stack == []

    def size(self):
        return len(self.stack)

    def print_regex_stack(self):
        print("---------------")
        for el in self.stack:
            el.print_tree(0)
            print("---------------")