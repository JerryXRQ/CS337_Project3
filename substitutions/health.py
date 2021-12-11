class Health():

    def __init__(self):
        self.attrs = ['vegan', 'healthy', 'unhealthy', 'gluten_free', 'lactose_free']
        self.vegan = {
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
        self.healthy = {
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
        self.unhealthy = {
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
        self.gluten_free = {
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
        self.lactose_free = {
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

    def __str__(self):
        result = ''
        for x in self.attrs:
            dic = getattr(self, x)
            result += f'{x}: '
            for key, value in dic.items():
                result +=key +' -> '+value+', '
            result = result[:len(result) - 2]
            result += f'; \n'
        return result
