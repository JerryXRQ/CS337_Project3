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
    question = ["can you","how can","how to","what is","walk me through", "i want"]
    for ele in question:
        if ele in input:
            return True
    return False

def search_youtube(question):
    query="https://www.youtube.com/results?search_query="
    return query+question.replace(" ","+")

def search_google(question):
    query = "https://www.google.com/search?q="
    return query + question.replace(" ", "+")

def handle_steps(rec):
    lib=rec.get_steps()
    step=0
    done=False
    while step<len(lib) and not done:
        if step%10==0:
            print("The " +str(step+1)+"-st step is: "+lib[step]["raw"])
        elif step%10==1:
            print("The " +str(step+1)+"-nd step is: "+lib[step]["raw"])
        elif step%10==2:
            print("The " +str(step+1)+"-rd step is: "+lib[step]["raw"])
        else:
            print("The " +str(step+1)+"-th step is: "+lib[step]["raw"])

        action=input()
        action=action.lower()
        if(question(action)):
            if "this" in action or "that" in action:
                if "what" in action:
                    if len(lib[step]["tools"])==0:
                        print("Sorry, I do not know what you are referring to.")
                    elif len(lib[step]["tools"])==1:
                        query=search_google("what is "+lib[step]["tools"][0])
                        print("I found the following results for you: "+query)
                    else:
                        print("Which one of these actions are you referring to: ", lib[step]["tools"])
                        choice=input()
                        query=search_google("how to "+choice)
                        print("I found the following results for you: " + query)
                else:
                    if len(lib[step]["methods"])==0:
                        print("Sorry, I do not know what you are referring to.")
                    elif len(lib[step]["methods"])==1:
                        query=search_youtube("how to "+lib[step]["methods"][0])
                        print("I found the following results for you: "+query)
                    else:
                        print("Which one of these actions are you referring to: ", lib[step]["methods"])
                        choice=input()
                        query=search_youtube("how to "+choice)
                        print("I found the following results for you: " + query)
            else:
                if "what" in action:
                    query = search_google(action)
                    print("I found the following results for you: " + query)
                else:
                    query = search_youtube(action)
                    print("I found the following results for you: " + query)
        elif "next" in action:
            if step+1==len(lib):
                print("you have reached the end of the recipe.")
            else:
                step+=1
        elif "previous" in action:
            if step-1<0:
                print("You are at the start of the recipe.")
            else:
                step-=1
        elif "go to" in action:
            jump=False
            while not jump:
                q = action.split()
                update = -1
                for ele in range(len(q)):
                    if q[ele]=="step":
                        try:
                            update=int(q[ele+1])
                        except:
                            print("I cannot find a vlaid number. Please enter a number in range [1, "+str(len(lib))+"]")
                    elif q[ele].isdigit():
                        update=int(q[ele])
                if update==-1 or update<1 or update>=len(lib):
                    print("Please enter a number in range [1, " + str(len(lib)) + "]")
                    action=input()
                else:
                    step=update-1
                    jump=True
        elif "how much" in action or "how many" in action:
            kw=action.split()
            start=0
            end=len(kw)
            for ele in range(len(kw)):
                if kw[ele]=="much" or kw[ele]=="many":
                    if ele+1< len(kw) and kw[ele+1]=="of":
                        start=ele+2
                    else:
                        start=ele+1
                elif kw[ele]=="do" or (end==len(kw) and kw[ele]=="i"):
                    end=ele
            target=" ".join(kw[start:end])
            ing=rec.get_ingredients()
            if target in ing:
                print("You need " + str(ing[target]["quantity"])+" "+ing[target]["unit"]+" of "+ target)
            else:
                match=[]
                source=set(target.split())
                for keys in ing:
                    for w in keys.split():
                        if w in source and keys not in ing:
                            match.append(keys)
                if len(match)==1:
                    print("You need " + str(ing[match[0]]["quantity"]) + " " + ing[match[0]]["unit"] + " of " + target)
                else:
                    print("which one of ",match," are you referring to?")
                    found=False
                    while not found:
                        choice=input()
                        if choice in match:
                            print("You need " + str(ing[match[0]]["quantity"]) + " " + ing[match[0]][
                                "unit"] + " of " + target)
                            found=True
                        else:
                            print("Please enter a valid choice")
        elif "temperature" in action:
            if "degrees" not in lib[step]["raw"]:
                print("Sorry, I cannot find valid temperature information")
            else:
                sp=lib[step]["raw"].split()
                C=""
                F=""
                for i in range(len(sp)):
                    if sp[i] == "degrees":
                        if i<len(sp)-1 and sp[i+1]=="f":
                            F=" ".join(sp[i-1:i+2])
                        elif i<len(sp)-1 and sp[i+1]=="c)":
                            C=" ".join(sp[i-1:i+2])
                print("The temperature you need is "+F+" "+C)
        elif "how long" in action or "when" in action:
            if "time" in lib[step]:
                print("It takes " +str(lib[step]["time"]["quantity"])+" "+str(lib[step]["time"]["unit"]))
            else:
                print("Sorry, the parser cannot find time information")



        elif finish(action):
            done=True



def main():
    my_recipe=None
    print("Welcome to Recipe Master")
    text=input()
    text=text.lower()
    while not finish(text):
        if greet(text):
            print("Hello. How can I help you?")

        elif question(text) and my_recipe==None:
            print("Sure, please enter a URL from AllRecipes.com")
            valid=False
            done=False
            while not valid:
                url=input()
                if len(url)<4 or "http" not in url:
                    print("Please enter a valid url")
                elif finish(url):
                    done=True
                    break
                else:
                    url=url[url.find('http'):]
                    print("Processing the recipe now")
                    try:
                        my_recipe=parse_tools.recipe(url)
                        print("I have processed "+my_recipe.get_title()+" for you. What can I do now")
                        print("What action do you want to perform: [1] Go over ingredients list or [2] Go over recipe steps.")
                        valid=True
                    except:
                        print("Sorry, the url entered does not seem to work. Please try again.")
            if done:
                break
            #Recipe Initialization

            choice=input()
            processed=False
            while not processed:
                if choice=="1":
                    print("The following ingredients are required by this recipe: ")
                    my_recipe.print_ingredients()
                    print("What else can I do?")
                    response=input()
                    if "step" in response or "procedure" in response:
                        choice="2"
                    else:
                        processed=True
                elif choice=="2":
                    handle_steps(my_recipe)
                    processed=True
                else:
                    print("Please enter either 1 or 2 to proceed")
                    choice=input()
            if processed:
                break
            #Recipe handling

        text=input()
    print("Thank you for using Recipe Master. Have a nice day.")
    return


if __name__ == '__main__':
    main()
