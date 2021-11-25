import parse_tools
import sys, os

# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__


recipes = \
[
    "https://www.allrecipes.com/recipe/12504/brown-familys-favorite-pumpkin-pie/",
    "https://www.allrecipes.com/recipe/147103/delicious-egg-salad-for-sandwiches/",
    "https://www.allrecipes.com/recipe/228875/maple-roasted-brussels-sprouts-with-bacon/",
    "https://www.allrecipes.com/recipe/258247/moo-shu-vegetable-stir-fry/",
    "https://www.allrecipes.com/recipe/103088/wisconsin-five-cheese-bake/",
    "https://www.allrecipes.com/recipe/229809/slow-cooker-green-bean-casserole/",
    "https://www.allrecipes.com/recipe/244796/labneh-lebanese-yogurt/",
    "https://www.allrecipes.com/recipe/246628/spaghetti-cacio-e-pepe/",
    "https://www.allrecipes.com/recipe/242402/greek-lemon-chicken-and-potato-bake/",
    "https://www.allrecipes.com/recipe/257938/spicy-thai-basil-chicken-pad-krapow-gai/",
    "https://www.allrecipes.com/recipe/143069/super-delicious-zuppa-toscana/",
    "https://www.allrecipes.com/recipe/257865/easy-chorizo-street-tacos/",
    "https://www.allrecipes.com/recipe/236703/chef-johns-chicken-kiev/",
    "https://www.allrecipes.com/recipe/236411/indian-style-chicken-and-onions/",
    "https://www.allrecipes.com/recipe/259373/chiles-en-nogada-mexican-stuffed-poblano-peppers-in-walnut-sauce/",
    "https://www.allrecipes.com/recipe/260815/russian-cabbage-rolls-with-gravy/",
    "https://www.allrecipes.com/recipe/273786/spicy-korean-fried-chicken-with-gochujang-sauce/", 
    "https://www.allrecipes.com/recipe/282702/spicy-breakfast-quesadillas/",
    "https://www.allrecipes.com/recipe/259887/simple-teriyaki-sauce/"
]
transforms = ["original.to_Vegetarian()", 
              "original.weight()", 
              "original.to_Non_Vegetarian()", 
              "original.to_Healty()", 
              "original.to_Unhealthy()", 
              "original.scale(2.0)", 
              "original.scale(0.5)", 
              "original.gluten_free()", 
              "original.lactose_free()", 
              "original.lactose_free()",
              "original.chinese()",
              "original.kosher()",  
              "original.to_Vegan()", 
              "original.mexico()", 
              "original.cajun()",
              "original.french()",
              "original.indian()",
              "original.to_stir_fry()", 
              "original.to_deep_fry()", 
              "original.original_cuisine()",
              "original.to_bake()",
              "original.to_steam()",
              "original.print_title()",
              "original.print_methods()"
            ]

for i in recipes:
    for j in transforms:
        blockPrint()
        original = parse_tools.recipe(i)
        try:
            blockPrint()
            eval(j)
        except: 
            enablePrint()
            print("Failure on recipe:   ", i, "using function:  ", j)
        del original

    enablePrint()
    print("Tested ", i, "on all transformations without error")
    blockPrint()
enablePrint()
print("finished")