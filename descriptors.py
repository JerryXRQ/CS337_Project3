class descriptors():

    def __init__(self):
        self.attrs = ['preparation', 'food', 'style', 'seasoning', 'other']
        self.preparation = [
                              "al dente",
                              "allumette",
                              "battered",
                              "baton",
                              "batonnet",
                              "beaten",
                              "bias",
                              "blackened",
                              "blanched",
                              "blended",
                              "boiled",
                              "boned",
                              "braised",
                              "brewed",
                              "broiled",
                              "browned",
                              "brunoise",
                              "caked",
                              "chopped",
                              #"canned",
                              "charred",
                              "chilled",
                              "chiffonade"
                              "chopped",
                              "cored",
                              "creamed",
                              "crumbled",
                              "crushed",
                              "cubed",
                              "cured",
                              "curried",
                              "cut",
                              "deglazed",
                              "dehydrated",
                              "debone",
                              "deboned",
                              "devein",
                              "deviled",
                              "diced",
                              "dice",
                              "divided",
                              "drained",
                              #"dried",
                              "escalloped",
                              "evaporated",
                              "fermented",
                              "flambé",
                              "fricassed",
                              "grated",
                              "ground",
                              "halved",
                              "julienned",
                              "mashed",
                              "melted",
                              "minced",
                              "mince",
                              "peeled",
                              "pitted",
                              "removed",
                              "reserved",
                              "rinsed",
                              "roasted",
                              "rubbed",
                              "reduced",
                              "seasoned",
                              "seeded",
                              "separated",
                              "shredded",
                              "sliced",
                              "soaked",
                              "softened",
                              "stemmed",
                              "thawed",
                              "thawed",
                              "torn",
                              "patted",
                              "quartered",
                              "trimmed",
                              "zested",
                              "juiced",
                              "lightly"
                            ]
        self.food = [
            "boneless",
            "instant",
            "lean",
            "lukewarm",
            "raw",
            "marbled",
            "refrigerated",
            "skinless",
            "halves",
            "skin",
            "bone",
            "breast",
            "neck",
            "giblets"
      ] + [
            "condensed",
            "fresh",
            "large",
            "organic",
            "packed",
            "ripe",
            "very ripe",
            "flat-leaf"
      ] + [
            "cooked",
            "freshly",
            "frozen"
      ] + [
            "skim",
            "whole"
      ]
        self.seasoning = [
            "seasoning",
            "active",
            "all purpose",
            "boiling",
            "distilled",
            "dry",
            "extra firm",
            "extra virgin",
            "frying",
            "ground",
            "hickory flavored",
            "low sodium",
            "non dairy",
            "nonfat",
            "reduced sodium",
            "room temperature",
            "superfine",
            "sweetened",
            "unsweetened",
            "black"
      ]
        self.style = [
            "african",
            "albanian",
            "algerian",
            "american",
            "andorrian",
            "argentinean",
            "argentinian",
            "armenian",
            "australian",
            "austrian",
            "bangladesh",
            "barbados",
            "belarus",
            "belgian",
            "belize",
            "bolivian",
            "brazilian",
            "british",
            "bulgarian",
            "cambodian",
            "canadian",
            "chad",
            "chilean",
            "chinese",
            "colombian",
            "costa rica",
            "creole",
            "croatian",
            "cuban",
            "dominican",
            "egyptian",
            "el salvadorian",
            "english",
            "estonian",
            "ethiopian",
            "finnish",
            "florentine",
            "french",
            "georgian",
            "german",
            "greek",
            "guatemalan",
            "hungarian",
            "indian",
            "indonesian",
            "iranian",
            "irish",
            "israeli",
            "italian",
            "japanese",
            "kenyan",
            "korean",
            "kosher",
            "liberian",
            "libyan",
            "lithuanian",
            "malaysian",
            "mediterranean",
            "mexican",
            "mongolian",
            "moroccan",
            "nigerian",
            "norwegian",
            "peruvian",
            "phillippino",
            "polish",
            "portuguese",
            "puerto rican",
            "romanian",
            "russian",
            "samoan",
            "serbian",
            "sichuan",
            "singapore",
            "slovakian",
            "somalian",
            "south african",
            "spanish",
            "sudanese",
            "swedish",
            "swiss",
            "syrian",
            "szechuan",
            "taiwanese",
            "thai",
            "tunisian",
            "turkish",
            "ukrainian",
            "venezuelan",
            "vietnamese"
      ]
        self.other = [
            "whole",
            "finger-sized",
            "all-purpose",
            "a la carte",
            "a la king",
            "a la mode",
            "acid",
            "acidic",
            "acrid",
            "airy",
            "alcoholic",
            "ambrosial",
            "aromatic",
            "au fromage",
            "au gratin",
            "au jus",
            "balsamic",
            "bite size",
            "bitter",
            "blah",
            "bland",
            "bold",
            "bolognese",
            "brackish",
            "briny",
            "brittle",
            "bubbly",
            "burning",
            "bursting",
            "buttery",
            "béarnaise",
            "cacciatore",
            "cakey",
            "candied",
            "carmelized",
            "caustic",
            "chalky",
            "charcuterie",
            "cheesy",
            "chewy",
            "chipotle",
            "chocolately",
            "classical",
            "crispy",
            "crumbly",
            "crunchy",
            "crusty",
            "crystalized",
            "curdled",
            "cold",
            "cubes",
            "dark",
            "decadent",
            "delactable",
            "dense",
            "diluted",
            "distinctive",
            "doughy",
            "dredged",
            "dried out",
            "dry",
            "earthy",
            "fatty",
            "feathery",
            "fibrous",
            "fiery",
            "finely",
            "filled",
            "filling",
            "finger licking good",
            "fishy",
            "fizzy",
            "flakey",
            "floury",
            "fluffy",
            "folded",
            "fragrant",
            "fried",
            "unsalted",
            "uncooked",
            "strips",
            "thinly",
            "slices",
            "hard",
            "extra-virgin",
            "seedless",
            "room",
            "temperature",
            "room-temperature"
      ] + [
            "boneless",
            "instant",
            "lean",
            "lukewarm",
            "raw",
            "marbled",
            "refrigerated",
            "skinless",
            "halves",
            "skin",
            "bone",
            "breast",
            "neck",
            "giblets",
            "unbaked",
            "prepared",
            "whole",
            "finger-sized",
            "all-purpose",
            "a la carte",
            "a la king",
            "a la mode",
            "acid",
            "acidic",
            "acrid",
            "airy",
            "alcoholic",
            "ambrosial",
            "aromatic",
            "au fromage",
            "au gratin",
            "au jus",
            "balsamic",
            "bite size",
            "bitter",
            "blah",
            "bland",
            "bold",
            "bolognese",
            "brackish",
            "briny",
            "brittle",
            "bubbly",
            "burning",
            "bursting",
            "buttery",
            "béarnaise",
            "cacciatore",
            "cakey",
            "candied",
            "carmelized",
            "caustic",
            "chalky",
            "charcuterie",
            "cheesy",
            "chewy",
            "chipotle",
            "chocolately",
            "classical",
            "crispy",
            "crumbly",
            "crunchy",
            "crusty",
            "crystalized",
            "curdled",
            "cold",
            "cubes",
            "chunks",
            "dark",
            "decadent",
            "delactable",
            "dense",
            "diluted",
            "distinctive",
            "doughy",
            "dredged",
            "dried out",
            "dry",
            "earthy",
            "fatty",
            "feathery",
            "fibrous",
            "fiery",
            "finely",
            "filled",
            "filling",
            "finger licking good",
            "fishy",
            "fizzy",
            "flakey",
            "floury",
            "fluffy",
            "folded",
            "fragrant",
            "fried",
            "unsalted",
            "strips",
            "thinly",
            "slices",
            "toasted",
            "hard",
            "plain",
            "extra-virgin",
            "seedless",
            "pieces",
            "cooked",
            "freshly",
            "frozen",
            "garnish"
            "active",
            "all purpose",
            "boiling",
            "distilled",
            "dry",
            "extra firm",
            "extra virgin",
            "frying",
            "ground",
            "hickory flavored",
            "low sodium",
            "non dairy",
            "nonfat",
            "reduced sodium",
            "room temperature",
            "superfine",
            "sweetened",
            "unsweetened",
            "black"
            "condensed",
            "fresh",
            "large",
            "organic",
            "packed",
            "ripe",
            "very ripe",
            "flat-leaf"
            "skim",
            "whole",
            "unpeeled",
            "room",
            "temperature",
            "kosher",
            "thick",
            "bulk",
            "mild",
            "uncooked"
]

    def __str__(self):
        result = ''
        for x in self.attrs:
            result += f'{x}: {getattr(self, x)};'
        return result
