class Command:
    def execute(self):
        raise NotImplementedError

    def undo(self):
        pass
