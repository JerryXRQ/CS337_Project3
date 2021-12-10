class Style():

    def __init__(self):
        self.attrs = []
        pass

    def __str__(self):
        result = ''
        for x in self.attrs:
            dic = getattr(self, x)
            result += f'{x}: '
            for key, value in dic.items():
                result += 'key -> value, '
            result += f'; \n'
        return result
