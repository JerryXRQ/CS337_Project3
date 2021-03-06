'''Version 0.35'''
from bs4 import BeautifulSoup
import requests
from collections import defaultdict


Liquid_Measurements=set(["Tbsp",
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
      "scoops"])
Solid_Measurements=set([
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
])

prep=set( [
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
      "flamb??",
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
    ])

descriptors= {
      "meat": set([
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
      ]),
      "other": set([
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
            "b??arnaise",
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
      ]),
      "seafood": set([
            "cooked",
            "freshly",
            "frozen"
      ]),
      "seasoning": set([
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
      ]),
      "style": set([
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
      ]),
      "veggie": set([
            "condensed",
            "fresh",
            "large",
            "organic",
            "packed",
            "ripe",
            "very ripe",
            "flat-leaf"
      ]),
      "dairy":set([
            "skim",
            "whole"
      ])
      }

Region=\
{
      "US/Canada":set([
            "cheese curds", "yeast", "macaroni", 
            "potatos", "hot dogs", "franks", 
            "buttermilk", "andouille", "butter",
            "turkey", "collard greens", "pecans", 
            "american cheese", "corn", "blueberries", 
            "okra", "pumpkin", "cornmeal", 
            "monterey jack", "cactus", "maple", 
            "pecans", "cranberry", "apple"
            ]),
      "Central/South America":set([
            "plantain", "potato", "potatos", 
            "cilantro", "quinoa", "jalepeno", 
            "papaya", "yuca", "yucca", 
            "masa" "tortilla", "oaxaca", 
            "oregano", "cassava", "cubanelle", 
            "avocados", "limes", "queso fresco", 
            "corn", "tomatoes", "tomatillo", 
            "flour tortillas", "corn tortillas", 
            "tomatillos", "chipotle", "chipotles", 
            "adobo", "salsa", "cactus", 
            "chorizo", "poblano peppers", "tortilla chips",
            "tomato"
            ]),
      "Europe":set([
            "yeast", "apple", "wine", 
            "cucumber", "rosemary", "cream",
            "creme", "leek", "chard", 
            "carrot", "tarragon", "celery", 
            "butter", "barley", "pasta", 
            "polenta", "bratwurst", "beet", 
            "turnip", "potatoes", 
            "potato", "carrots",  ]),
      "Mediterranean/MiddleEastern":set([
            "yeast", "cucumber", "artichoke", 
            "lemon", "olive", "yogurt", 
            "pecorino", "mozzarella", "mint", 
            "ricotta", "feta", "dill", 
            "phyllo", "spinach", "olive oil", 
            "harissa", "eggplant", "parmesean", 
            "beans", "balsamic", "reggiano", 
            "parsley", "basil", "yogurt", 
            "lamb", "saffron", "Pecorino Romano cheese",
            "spaghetti", "Parmigiano-Reggiano cheese"]),
      "African":set([
            "okra", "millet", "tamarind",
            "palm oil", "coconut", "harissa",
            "couscous", "pistachios", "cumin",
            "mint", "saffron", "yams", "sweet potatoes",
            "preserved lemon", "ginger", "turmeric", 
            "parsley", "lentil", "tomatoes", "tomato", "lamb"
            ]),
      "South Asian":set([
            "coriander", "cardamom", "cloves", 
            "turmeric",  "garum", "curry", 
            "ghee", "basmati", "lentils", 
            "ginger", "mustard seed", "mustard seeds", 
            "kashmiri", "coconut", "paneer", 
            "cumin", "curry", "cinnamon", 
            "lemongrass", "basil", "jicama", 
            "vermicelli", "daikon", "bean sprouts", 
            "galangal", "mango", "fish sauce", 
            "peanuts", "cilantro", 'garam masala',
            "panko bread crumbs", 
            ]),
      "East Asian":set([
            "soy", "soy sauce", "sesame oil", 
            'sesame', "wasabi", "dashi", 
            "kombu", "nori", "miso", 
            "panko", "green onion", "oyster sauce", 
            "tofu", "mirin", "sake", 
            "gochugaru", "gochujang", "kimchi", 
            "shiitake", "bok choy", "ginger", 
            "mungbean", "daikon", "scallion",
            "hoisin", "bamboo",  "Szechuan peppercorns", 
            "sesame seeds", 'scallion'
            ]),
}


descriptors_non_nation=set([
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
            "b??arnaise",
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
])
      

Method_Primary=set([
      "bake",
      "boil",
      "broil",
      "blanch",
      "microwave",
      "stir-fry",
      "fry",
      "pressure cook",
      "grill",
      "simmer",
      "blend",
      "sear",
      "steam",
      "saute",
      "poach",
      "deep-fry",
      "shallow-fry",
      "roast",
      "slow-cook",
      "slow cook"
    ])
Tools_to_Method={
      "air-fryer":"air-fry",
      "fryer":"fry",
      "wok":"stir-fry",
      "pressure cooker":"pressure cook"
}

Method_Secondary=set([
      "arrange",
      "add",
      "bake",
      "beat",
      "boil",
      "brush",
      "cover",
      "cool",
      "combine",
      "cream",
      "cut",
      "crush",
      "dip",
      "drain",
      "dry",
      "chill",
      "crumble",
      "flour",
      "flip",
      "fold",
      "grease",
      "grate",
      "heat",
      "line",
      "mash",
      "measure",
      "mix",
      "melt",
      "pour",
      "garnish",
      "preheat",
      "pound",
      "layer",
      "stuff",
      "knead",
      "refrigerate",
      "rinse",
      "saute",
      "serve",
      "season",
      "shake",
      "squeeze",
      "simmer",
      "sift",
      "slice",
      "soak",
      "spoon",
      "spread",
      "sprinkle",
      "stir",
      "strain",
      "toast",
      "toss",
      "turn",
      "whisk",
      "coat",
      "place",
      "rub",
      "lower"
    ])
Tools=set([
    "apple corer",
    "apple cutter",
    "bag",
    "baking sheet",
    "balloon whisk",
    "basket skimmer",
    "baster",
    "basting brush",
    "beanpot",
    "bell whisk",
    "bench knife",
    "bench scraper",
    "biscuit mould",
    "blender",
    "blow torch",
    "blowlamp",
    "blowtorch",
    "boil oven preventer",
    "bottle opener",
    "bowl",
    "bread knife",
    "browning bowl",
    "browning plate",
    "browning tray",
    "bulb baster",
    "burger spatula",
    "burr grinder",
    "burr mill",
    "buscuit cutter",
    "buscuit press",
    "butcher's twine",
    "butter curler",
    "cake server",
    "cake shovel",
    "can opener",
    "candy thermometer",
    "carving knife",
    "cheese cutter",
    "cheese grater",
    "cheese knife",
    "cheese knives",
    "cheese slicer",
    "cheese spreader",
    "cheesecloth",
    "chef knife",
    "chef's knife",
    "chefs knife",
    "cherry pitter",
    "chinois",
    "chinoise",
    "citrus reamer",
    "clay pot",
    "cleaver",
    "colander",
    "cookie cutter",
    "cookie mould",
    "cookie press",
    "cooking twine",
    "corkscrew",
    "crab cracker",
    "cup",
    "cutting board",
    "deep spoon",
    "dish",
    "dough scraper",
    "drum sieve",
    "dutch oven",
    "edible tableware",
    "egg piercer",
    "egg poacher",
    "egg separator",
    "egg slicer",
    "egg timer",
    "fat separator",
    "fillet knife",
    "fish scaler",
    "fish slice",
    "fish spatula",
    "flat coil whisk",
    "flat whisk",
    "flour sifter",
    "food mill",
    "food storage container",
    "french whisk",
    "frying pan",
    "funnel",
    "fryer",
    "garlic press",
    "grapefruit knife",
    "grater",
    "gravy separator",
    "gravy strainer",
    "gravy whisk",
    "griddle",
    "herb chopper",
    "honey dipper",
    "ice cream scoop",
    "kitchen mallet",
    "kitchen scale",
    "kitchen scissor",
    "kitchen scraper",
    "kitchen string",
    "kitchen tool crock",
    "kitchen twine",
    "knife",
    "ladle",
    "lame",
    "lemon reamer",
    "lemon squeezer",
    "lobster fork",
    "lobster pick",
    "mandoline",
    "mashers",
    "mated colander pot",
    "measuring cup",
    "measuring jar",
    "measuring jug",
    "measuring spoon",
    "meat grinder",
    "meat tenderiser",
    "meat tenderizer",
    "meat thermometer",
    "melon ball",
    "melon baller",
    "metal tong",
    "mezzaluna",
    "microplane",
    "milk frother",
    "milk guard",
    "milk watcher",
    "mincer",
    "mini whisk",
    "mixing bowl",
    "mixing whisk",
    "molcajete",
    "mortar",
    "nutcracker",
    "nutmeg grater",
    "olive stoner",
    "oven glove",
    "oven mitt",
    "oven",
    "pan",
    "panini spatula",
    "pasta fork",
    "pastry bag",
    "pastry blender",
    "pastry brush",
    "pastry wheel",
    "paper towel",
    "peeler",
    "pepper grinder",
    "pepper mill",
    "pestle",
    "pie bird",
    "pie cutter",
    "pie funnel",
    "pie server",
    "pie vent",
    "pizza cutter",
    "pizza shovel",
    "pizza slicer",
    "pot holder",
    "pot minder",
    "pot",
    "pot-holder",
    "potato masher",
    "potato ricer",
    "potholder",
    "poultry shears",
    "ricer",
    "roast lifter",
    "roller docker",
    "rolling pin",
    "salt shaker",
    "santoku knife",
    "saucepan",
    "scale",
    "scissor",
    "scoop",
    "scraper",
    "serrated bread knife",
    "serving platter",
    "shredder",
    "sieve",
    "sifter",
    "silicone tong",
    "skillet",
    "slotted spoon",
    "spatula",
    "spider strainer",
    "spider",
    "spoon sieve",
    "spoon skimmer",
    "steak knife",
    "stove",
    "strainer",
    "sugar thermometer",
    "slow cooker",
    "tablespoon",
    "tamis",
    "teaspoon",
    "tin opener",
    "tomato knife",
    "tong",
    "trussing needle",
    "turner",
    "twine",
    "urokotori",
    "utility knife",
    "vegetable peeler",
    "weighing scales",
    "whisk",
    "wooden spoon",
    "zester",
    "nonstick spray"
])
Time_Units=set([
      "second",
      "seconds",
      "minute",
      "minutes",
      "hour",
      "hours",
      "day",
      "days"
])
Vegan_Protein=set([
      "cauliflower",
      "lentils",
      "tempeh",
      "king oyster mushrooms",
      "cabbage",
      "tofu",
      "chickpeas",
      "black beans",
      "pinto"
])
Non_Vegan={"meat":[
      "beef",
      "pork",
      "lamb",
      "chicken",
      "duck",
      "turkey",
      "fish",
      "cod",
      "crab",
      "clam",
      "mussels",
      "shrimp",
      "salmon",
      "tuna",
      "tilapia",
      "rib",
      "sirloin",
      "brisket",
      "bacon",
      "bison",
      "goose",
      "mutton",
      "venison",
      "catfish",
      "ham",
      "lobster",
      "octopus",
      "luncheon meat"
]}

Vegetable=set([
      "potatoes",
      "potato",
      "tomatoes",
      "tomato",
      "onion",
      "onions",
      "carrots",
      "lettuce",
      "bell peppers",
      "broccoli",
      "cucumbers",
      "celery",
      "mushrooms",
      "mushroom",
      "corn",
      "spinach",
      "green beans",
      "cauliflower",
      "cabbage",
      "asparagus",
      "brussel sprouts",
      "crookneck",
      "edamame",
      "eggplant",
      "pumkin",
      "chickpeas"
])
#Intentionally ignored ingredients that serve as seasonings.
Vegan={
      "milk powder":"almond milk powder",
      "milk":"soy milk",
	  "mozzarella cheese": "vegan mozzarella cheese",
      "mozzarella": "vegan mozzarella",
      "parmesan cheese": "vegan parmesan cheese",
      "cheese": "crumbled tofu",
      "butter": "vegan margarine",
      "yogurt": "almond milk yogurt",
      "sour cream":"vegan sour cream",
      "heavy cream":"coconut cream",
      "scrambled egg": "tofu scramble",
      "egg whites":'tofu',
      "egg white":"tofu",
      "egg yolk": "tofu",
      "egg": "tofu",
      "yolk": "tofu",
      "instant pudding": "dairy free instant pudding",
      "pudding": "dairy free pudding",
      "sour cream": "vegan sour cream",
      "mayonnaise": "vegan mayonnaise",
      "ketchup": "vegan ketchup",
      "gelatin": "agar flakes",
      "honey": "agave nectar",
      "chocolate": "non-dairy chocolate",
      "hollandaise sauce": "vegan hollandaise sauce",
      "oyster sauce": "vegetarian oyster sauce",
      "worcestershire sauce": "organic worcestershire sauce",
      "bread": "wheat tortilla",
      "bread toasts": "wheat tortilla",
      "bagel": "vegan bagel",
      "pancake": "vegan pancake",
      "eggs":"tofu"
}

Make_Healthy={"approach":{
      "fry":"air-fry",
      "grill":"broil"
      },
      "tools":{
            "fryer":"air-fryer",
            "grill":"oven"
      }
      ,
      "ingredients":{
            "sugar":"honey",
            "white sugar":"honey",
            "brown sugar":"honey",
            "sour cream":"greek yogurt",
            "flour":"whole wheat flour",
            "butter":"margarine",
            "whole milk":"skim milk",
            "peanut butter":"powdered peanut",
            "baking powder":"baking soda",
            "chocolate":"berries",
            "cream cheese":"fat-free cream",
            "mayonnaise":"plain yogurt",
            "mayo":"plain yogurt",
            "white bread":"wheat bread",
            "sausage":"bacon",
            "egg":"egg white",
            "pasta":"whole grain pasta",
            "spaghetti":"whole grain spaghetti",
            "potato":"cauliflower",
            "potatoes":"cauliflowers",
            "pork":"beef",
            "noodles":"zucchini noodles",
            "potato chips":"popcorn",
            "ranch dressing":"balsamic vinegar",
            "salami":"low-sodium ham",
            "pickle":"cucumber",
            "cheese":"low-fat cheese",
            "margarine":"diet margarine",
            "turkey bacon":"fresh turkey stripes",
            "chocolate":"carob",
            "beef":"extra-lean beef",
            "soy sauce":"low-sodium soy sauce"
      }
}

Make_Unhealthy={"approach":{
      "broil":"grill",
      "steam":"fry",
      "saute":"fry"
      },
      "tools":{
            "steamer":"deep fryer",
            "oven":"grill",
            "pan":"deep fryer"
      }
      ,
      "ingredients":{
            "honey":"sugar",
            "sweet potato":"potato",
            "beef":"pork",
            "chicken":"pork",
            "salmon":"pork",
            "mushroom":"pork",
            "milk":"creamer",
            "bacon":"sausage",
            "hummus":"mayo",
            "broccoli":"potato",
            "bell pepper":"bacon",
            "cauliflower":"potato",
            "edamame":"sausage",
            "chickpeas":"sausage",
            "carrot":"potato",
            "jam":"sugar",
            "olive oil":"butter",
            "nuts":"chocolate",
            "greek yogurt":"sour cream",
            "cinnamon":"sugar",
            "applesauce":"sugar",
            "maple syrup":"sugar"
      }
}

meat=set([
      "beef",
      "pork",
      "lamb",
      "chicken",
      "duck",
      "turkey",
      "rib",
      "sausage",
      "sirloin",
      "brisket",
      "bacon",
      "bison",
      "goose",
      "mutton",
      "venison",
      "ham",
])

volume_to_gram={
      "tablespoon":14,
      "teaspoon":4,
      "teaspoons":4,
      "tablespoons":14,
      "cup":115,
      "cups":115
}

shellfish={
      "clams":"oyster mushroom",
      "mussels":"oyster mushroom",
      "oysters":"oyster mushroom",
      "scallops":"oyster mushroom",
      "shrimp":"oyster mushroom",
      "lobster":"oyster mushroom",
      "crayfish":"oyster mushroom",
      "crab":"oyster mushroom",
      "clams":"oyster mushroom"
}

Kosher={
      "pork":"beef",
      "sausage":"beef sausage",
      "lard":"tallow"
}

Gluten_Free={
      "farro":"rice",
      "barley":"quinoa",
      "bulgur":"millet",
      "spelt":"buckwheat",
      "kamut":"rice",
      "breadcrumbs":"chickpea crumbs",
      "noodle":"rice noodles",
      "noodles":"rice noodles",
      "pasta":"kelp noodles",
      "spaghetti":"spaghetti squash",
      "fettuccine":"veggie noodles",
      "macaroni":"kelp noodles",
      "bow ties":"rice noodles",
      "tortillas":"corn tortillas",
      "flour tortillas":"corn tortillas",
      "soy sauce":"coconut aminos",
      "pizza crust":"cauliflower crust",
      "flour":"rice flour",
      "rigatoni pasta":"kelp noodles",
      "macaroni":"spaghetti squash",
      "rigatoni":"kelp noodles"
}


Chinese = \
      {"approach":{
            "fry":"stir-fry",
            "saute":"stir-fry",
            "sear":"stir-fry",
            "soak":"boil",
            "immerse":"braise",
            "bath":"braise",
            "broil":"roast",
            "grill":"roast",
            "bake":"steam"
      },
      "tools":{
            "fork":"chopsticks",
            "spoon":"cooking shovel",
            "pan":"wok",
            "tray":"wok",
            "oven":"steamer"
      },
      "ingredients":{
            "chili":"dried chili",
            "hot pepper":"chili powder",
            #"pepper":"sichuan peppercorns",
            "pepper":"white pepper",
            "spice":"five spice powder",
            "parsley":"bay leaf",
            "coriander":"bay leaf",
            "seasoning":"parsley",
            "salt":"soy sauce",
            "lemon":"vinegar",
            "olive oil": "sesame oil",
            "butter":"sesame oil",
            "starch":"cornstarch",
            "bbq sauce":"oyster sauce",
            "tomato sauce":"hoisin sauce",
            "ketchup":"hosin sauce",
            #"cabbage":"bok choy",
            "cabbage":"napa cabbage",
            "mushroom":"shiitake mushroom",
            "mushrooms":"shiitake mushrooms",
            "cinnamon":"chinese five spice",
            "tomato sauce":"chilli bean sauce",
            "red chilli sauce":"chilli bean sauce",
            "mayonnaise":"chilli bean sauce",
            "mayo":"chilli bean sauce",
            "red wine":"shaoxing rice wine",
            "vinegar":"white rice vinegar",
            "pasta":"dried egg noodles",
            "spaghetti":"dried egg noodles"
            #"noodles":"vermicelli noodles"
      }
}

Cajun=\
{
      "approach":
      {
            "stir-fry":"saute",
            "steam":"smoke",

      },
      "tools":{
            "chopsticks":"fork",
            "steamer":"smoker"
      },
      "ingredients":
      {
            "miripoix":"holy trinity",
            "soffrito":"holy trinity",
            "carrot":"bell pepper",
            "roux":"dark roux",
            "shallot":"green onion",
            "chili":'cayenne',
            "sausage":"andouille",
            "chorizo":"boudin",
            "pork":"boar",
            "pork belly":"salt pork",
            "stew":"gumbo",
            "rice":"dirty rice"
      }

}

German=\
{
      "ingredients":
      {
            "sour cream":"schmandt",
            "beef":"veal",
            "fennel":"caraway"
      }
}


Mexican={
      "approach":{
            "bake":"roast",
            "wok":"plancha",
            "griddle":"plancha",
            "broil":"roast"
      },
      "tools":{
            "oven":"steamer",
            "spoon":"spatula"
      },
      "ingredients":{
            "pasta":"pinto",
            "spaghetti":"black beans",
            "flour":"rice flour",
            "potato":"avocado",
            "potatoes":"avocado",
            "basil":"cilantro",
            "parsley":"cilantro",
            "lemon":"lime",
            "soy sauce":"vinegar",
            "ketchup":"salsas",
            "broccoli":"corn",
            "cauliflower":"corn",
            "hot pepper":"jalapenos",
            "beef":"pork",
            "miripoix":"soffrito",
            "steak":"pork",
            "macaroni":"rice",
            "lasagne":"rice",
            "chiles":"guajillo chiles",
            "cinnamon":"mexican cinnamon",
            "chocolate":"mexican chocolate",
            "butter":"lard",
            "vegetable oil":"lard"
      }
}

Lactose_Free={
      "milk":"soy milk",
      "butter":"coconut oil",
      "cheese":"plant-based cheese",
      "hard cheese":"tofu",
      "ice cream":"sherbet",
      "yogurt":"coconut milk yogurt",
      "cream":"coconut milk",
      "heavy cream":"coconut milk",
      "whipping cream":"coconut milk",
      "sour cream":"nondairy yogurt"
}

Cook_Approach=set([
      "bake",
      "boil",
      "broil",
      "stir-fry",
      "fry",
      "pressure cook",
      "grill",
      "steam",
      "saute",
      "deep-fry",
      "roast"
])

Approach_Tools={
      "oven",
      "wok",
      "fryer",
      "pressure cooker",
      "grill",
      "steamer",
      "fry pan",
      "saucepan",
      "stock pot",
      "skillet",
      "griddle",
      "plancha",
      "deep-fryer"
}


Meat_Parts=set([
      "neck",
      "chuck",
      "shank",
      "brisket",
      "shank",
      "rib",
      "loin",
      "rump",
      "sirloin",
      "flank",
      "tail",
      "thigh",
      "thighs",
      "wing",
      "wings",
      "tenderloin",
      "drum stick",
      "breast",
      "breasts",
      "head",
      "belly",
      "leg",
      "legs",
      "hock",
      "totters"
])

Indian = \
      {"approach":{
            "steam":"dum (Indian steam)",
            "temper":"Tadka/Baghar (Indian temper)",
            "saut":"Bhunao (Indian saute)",
            "saute":"Bhunao (Indian saute)",
            "smoke":"Dhuanaar (Indian smoke)",
            "fry":"Talina/Talna (Indian deep fry)",
            "roast":"Tandoori (Indian roast)",
            "soak":"boil",
            "immerse":"braise",
            "bath":"braise",
            "broil":"roast",
            "grill":"roast",
            "bake":"dum (Indian steam)"
      },
      "tools":{
            "fork":"chopsticks",
            "spoon":"cooking shovel",
            "pan":"wok",
            "tray":"wok",
            "oven":"steamer",
            "container":"stainless steel spice container",
            "box":"stainless steel spice container",
            "pesetle": "stainless steel mortar",
            "spoon": "grinder",
            "blender": "strainer",
            "pot": "deep fry pan",
            "pan": "deep fry pan",
            "knive": "stainless stell knive"
      },
      "ingredients":{
            "chili":"dried chili",
            "hot pepper":"chili powder",
            "pepper":"black pepper",
            "spice":"cardamom",
            "parsley":"cassia bark",
            "coriander":"cassia bark",
            "seasoning":"cumin",
            "salt":"nutmeg and mace",
            "lemon":"vinegar",
            "olive oil": "sesame oil",
            "butter":"sesame oil",
            "starch":"cornstarch",
            "bbq sauce":"oyster sauce",
            "tomato sauce":"hoisin sauce",
            "ketchup":"hosin sauce",
            "cabbage":"napa cabbage",
            "mushroom":"shiitake mushroom",
            "mushrooms":"shiitake mushrooms",
            "tomato sauce":"chilli bean sauce",
            "red chilli sauce":"chilli bean sauce",
            "mayonnaise":"chilli bean sauce",
            "mayo":"chilli bean sauce",
            "vinegar":"white rice vinegar",
            "pasta":"dried egg noodles",
            "spaghetti":"dried egg noodles"
      }
}


French = \
      {"approach":{
            "flavor":"bouquet garni",
            "cut":"chiffonade cut",
            "drizzle":"coulis",
            "loose":"d??glacer",
            "degalz":"d??glacer",
            "reduc":"demi-glace",
            "prepare":"en papillote",
            "vegetable":"julienne vegetable",
            "brais":"mirepoix",
            "simmer":"mirepoix",
            "put":"mise en place",
            "thicken":"roux",
            "whisk":"roux",
            "fry":"saut??"
      },
      "tools":{
            "knife":"fish spatula",
            "board":"rimmed baking sheet",
            "pan":"braising pans",
            "tray":"rimmed baking sheet",
            "pot":"non-stick skillets",
            "paper":"silicone baking mat",
            "towel":"linen kitchen towels",
            "oven": "dutch oven",
            "bowl": "ramekins",
            "dish": "oval baking dish"
      },
      "ingredients":{
            "oil":"olive oil",
            "mustard":"dijon mustard",
            "salt":"fleur de sel",
            "cream":"cr??me fra??che",
            "mushroom":"herves de provence",
            "onion":"shallots",
            "garlic":"shallots",
            "bread":"french bread",
            "cheese":"french cheese"
      }
}
Substitution_General={
            "sugar":"honey",
            "white sugar":"honey",
            "brown sugar":"honey",
            "sour cream":"greek yogurt",
            "flour":"whole wheat flour",
            "butter":"margarine",
            "whole milk":"skim milk",
            "peanut butter":"powdered peanut",
            "baking powder":"baking soda",
            "chocolate":"cocoa",
            "cream cheese":"fat-free cream",
            "mayonnaise":"plain yogurt",
            "mayo":"plain yogurt",
            "white bread":"wheat bread",
            "sausage":"bacon",
            "egg":"egg white",
            "pasta":"whole grain pasta",
            "spaghetti":"whole grain spaghetti",
            "potato":"cauliflower",
            "potatoes":"cauliflowers",
            "pork":"beef",
            "noodles":"zucchini noodles",
            "potato chips":"popcorn",
            "ranch dressing":"balsamic vinegar",
            "salami":"low-sodium ham",
            "pickle":"cucumber",
            "cheese":"low-fat cheese",
            "margarine":"diet margarine",
            "turkey bacon":"fresh turkey stripes",
            "beef":"lamb",
            "soy sauce":"low-sodium soy sauce",
            "clams":"oyster mushroom",
            "mussels":"oyster mushroom",
            "oysters":"oyster mushroom",
            "scallops":"oyster mushroom",
            "shrimp":"fish",
            "lobster":"crab",
            "crayfish":"oyster mushroom",
            "crab":"shrimp",
            "clams":"fish",
            "honey":"sugar",
            "sweet potato":"potato",
            "chicken":"pork",
            "salmon":"pork",
            "mushroom":"pork",
            "milk":"creamer",
            "bacon":"sausage",
            "hummus":"mayo",
            "broccoli":"potato",
            "bell pepper":"bacon",
            "cauliflower":"potato",
            "edamame":"sausage",
            "chickpeas":"sausage",
            "carrot":"potato",
            "jam":"sugar",
            "olive oil":"vegetable oil",
            "nuts":"chocolate",
            "greek yogurt":"sour cream",
            "cinnamon":"sugar",
            "applesauce":"sugar",
            "maple syrup":"sugar",
            "beer":"chicken broth",
            "bread crumbs":"cracker crumbs",
            "brown sugar":"white sugar",
            "evaporated milk":"light cream",
            "lemon grass":"lemon zest",
            "onion":"shallots",
            "orange zest":"orange juice",
            "vinegar":"lemon juice",
            "wine":"beef broth",
            "yogurt":"sour cream"
}