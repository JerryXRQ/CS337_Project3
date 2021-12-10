class Quantity():

    def __init__(self):
        self.attrs = []
        pass

    def __str__(self):
        result = ''
        for x in self.attrs:
            result += f'{x}: {getattr(self, x)}; \n'
        return result