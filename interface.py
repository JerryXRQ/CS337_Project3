'''Version 0.35'''
from bs4 import BeautifulSoup
import requests
import parse_tools
import copy
import re


def search(dish):

    search_url = 'https://www.allrecipes.com/search/results/?wt=%s&sort=re'
    target_url = search_url % (dish.replace(" ", "+"))
    html = requests.get(target_url)
    bs = BeautifulSoup(html.content, features="html.parser")
    return bs


all_actions = ['verbose', "methods", 'vegetarian', 'vegan', "weight", 'meat', "kosher", 'healthy', 'unhealthy',
               'double', 'half', 'gluten', 'chinese', "mexican", "cajun", 'indian', 'french', 'lactose', 'stir-fry',
               'deep-fry', 'region', 'undo', 'steam', "bake"]
def print_actions():
    print('\n')
    print("Available actions: ")
    print("Result Display: [verbose, methods, region]")
    print("Ingredients Requirements: [vegetarian, vegan, kosher, meat, gluten, lactose]")
    print("Health Related: [healthy, unhealthy]")
    print("Quantity Change: [double, half, weight]")
    print("Style Change: [chinese, mexican, cajun, indian, french]")
    print("Cooking Method Change: [stir-fry, deep-fry, steam, bake]")
    print("Undo: [undo]")
    print('\n')

def finish(input):
    finish_words=["bye","done","that's all", "that's everything"]
    for ele in finish_words:
        if ele in input:
            return True
    return False

def greet(input):
    greetings=["hello","good morning","good afternoon","good evening","what's up","how are you","hi"]
    for ele in greetings:
        if ele in input:
            return True
    return False

def question(input):
    question = ["can you","how can","how to","what is","walk me through", "I want"]
    for ele in question:
        if ele in input:
            return True
    return False

def main():
    step=None
    step_content=None
    my_recipe=None
    text=input()
    text=text.lower()
    print("Welcome to Recipe Master")
    while not finish(text):
        if greet(text):
            print("Hello. How can I help you?")

        elif question(text) and my_recipe==None:
            print("Sure, please enter a URL from AllRecipes.com")
            valid=False
            while not valid:
                url=input()
                if len(url)<4 or "http" not in url:
                    print("Please enter a valid url")
                else:
                    url=url[url.find('http'):]
                    print("Processing the recipe now")
                    try:
                        my_recipe=parse_tools.recipe(url)
                        print("I have processed it for you. What can I do now")
                        valid=True
                    except:
                        print("Sorry, the url entered does not seem to work. Please try again.")



        text=input()
    return


if __name__ == '__main__':
    main()
