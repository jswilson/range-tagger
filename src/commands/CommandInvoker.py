from collections import deque

class CommandInvoker:
    def __init__(self):
        self.command_stack = deque()
        self.redo_stack = deque()

    def execute(self, command):
        ret = command.execute()

        if ret:
            self.command_stack.append(command)
        self.redo_stack.clear()

    def undo(self):
        if len(self.command_stack) == 0:
            return
        command = self.command_stack.pop()
        command.undo()
        self.redo_stack.append(command)

    def redo(self):
        if len(self.redo_stack) == 0:
            return
        command = self.redo_stack.pop()
        command.execute()
        self.command_stack.append(command)
