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

def main():
    print("Welcome to Recipe Master!")

    return


if __name__ == '__main__':
    main()
