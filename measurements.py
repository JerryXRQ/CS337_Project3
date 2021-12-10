class Measurements():

    def __init__(self):
        self.attrs = ['liquid', 'solid', 'time']
        self.liquid = ["Tbsp",
                      "Tbsps",
                      "bottle",
                      "bottles",
                      "c",
                      "cs",
                      "cup",
                      "cups",
                      "dessertspoon",
                      "dessertspoons",
                      "fl oz",
                      "fl ozs",
                      "fluid ounce",
                      "fluid ounces",
                      "fluid oz",
                      "fluid ozs",
                      "gal",
                      "gallon",
                      "gallons",
                      "gals",
                      "jar",
                      "jars",
                      "liter",
                      "liters",
                      "milliliter",
                      "milliliters",
                      "ml",
                      "mls",
                      "pint",
                      "pints",
                      "pt",
                      "pts",
                      "qt",
                      "qts",
                      "quart",
                      "quarts",
                      "tablespoon",
                      "tablespoons",
                      "teaspoon",
                      "teaspoons",
                      "tsp",
                      "tsps",
                      "scoops"]
        self.solid = [
                       "#",
                      "#s",
                      "bag",
                      "bags",
                      "bunch",
                      "bunches",
                      "can",
                      "cans",
                      "clove",
                      "cloves",
                      "cube",
                      "cubes",
                      "dash",
                      "dashes",
                      "envelope",
                      "envelopes",
                      "gram",
                      "grams",
                      "head",
                      "heads",
                      "inch",
                      "inches",
                      "kilogram",
                      "kilograms",
                      "lb",
                      "lbs",
                      "loaf",
                      "ounce",
                      "ounces",
                      "oz",
                      "ozs",
                      "package",
                      "packages",
                      "packet",
                      "packets",
                      "piece",
                      "pieces",
                      "pinch",
                      "pinches",
                      "pound",
                      "pounds",
                      "sheet",
                      "sheets",
                      "slice",
                      "slices",
                      "strip",
                      "strips"
                        ]
        self.time = [
                      "second",
                      "seconds",
                      "minute",
                      "minutes",
                      "hour",
                      "hours",
                      "day",
                      "days"
                     ]

    def __str__(self):
        result = ''
        for x in self.attrs:
            result += f'{x}: {getattr(self, x)};'
        return result