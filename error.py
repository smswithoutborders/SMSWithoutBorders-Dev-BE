class Conflict(Exception):
    def __init__(self, message='conflict'):
        self.message = message
        super().__init__(self.message)

class InternalServerError(Exception):
    def __init__(self, message='internal server error'):
        self.message = message
        super().__init__(self.message)