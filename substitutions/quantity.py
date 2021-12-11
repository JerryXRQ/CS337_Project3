class Quantity():

    def __init__(self):
        self.attrs = ['vol_to_grams']
        self.vol_to_grams = {
      "tablespoon":14,
      "teaspoon":4,
      "teaspoons":4,
      "tablespoons":14,
      "cup":115,
      "cups":115
}

    def __str__(self):
        result = ''
        for x in self.attrs:
            dic = getattr(self, x)
            result += f'{x}: '
            for key, value in dic.items():
                result += "1 "+ key + ' -> ' + str(value) +" grams, "
            result = result[:len(result) - 2]
            result += f'; \n'
        return result
