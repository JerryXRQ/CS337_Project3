import os
import time
import re
from slackclient import SlackClient
import parse_tools
import data

# instantiate Slack client
slack_client = SlackClient("This is a placeholder for the actual code. Uploading it to GitHub will cause deactivation of the app")
starterbot_id = "U02QAF2MQAE"

# constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
EXAMPLE_COMMAND = "do"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

def send_ingredients(rec):
    send("List of Ingredients: ")
    ing=rec.get_ingredients()
    for ele in ing.keys():
        send("Name: "+ ele)
        send("Quantity: "+str(ing[ele]["quantity"]))
        send("Unit: "+ str(ing[ele]["unit"]))
        send("Preparation: " + str(ing[ele]["prep"]))
        send("Descriptions: " + str(ing[ele]["descriptions"]))
        send("Additional Instruction: "+str(ing[ele]["additional"]))
    return


def finish(input):
    finish_words=["bye","done","that's all", "that's everything"]
    for ele in finish_words:
        if ele in input:
            return True
    return False

def question(input):
    question = ["can you","how can","how to","what is","walk me", "i want", "i'd", "i would", "how do i","how","what", "would"]
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

def greet(input):
    greetings=["hello","good morning","good afternoon","good evening","what's up","how are you","hi"]
    for ele in greetings:
        if ele in input:
            return True
    return False

def recipe_init():
    send("Sure, please enter a URL from AllRecipes.com")
    valid = False
    done = False
    my_recipe=None
    while not valid:
        url = get_input()
        url=url.replace(">","")
        if len(url) < 4 or "http" not in url:
            send("Please enter a valid url")
        elif finish(url):
            done = True
            break
        else:
            url = url[url.find('http'):]
            print(url)
            send("Processing the recipe now")
            try:
                my_recipe = parse_tools.recipe(url)
                send("I have processed " + my_recipe.get_title() + " for you. What can I do now")
                send("What action do you want to perform: [1] Go over ingredients list or [2] Go over recipe steps.")
                valid = True
            except:
                send("Sorry, the url entered does not seem to work. Please try again.")
    return done,my_recipe


def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == starterbot_id:
                return message, event["channel"]
    return None, None

def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def get_input():
    while True:
        command, channel = parse_bot_commands(slack_client.rtm_read())
        if command:
            return command


def send(message):
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=message
    )

def handle_command(command, channel):
    my_recipe = None
    send("Welcome to Recipe Master")
    send("How can I help you?")
    text = get_input()
    text = text.lower()
    while not finish(text):
        if greet(text):
            send("Glad to hear from you! How can I help you today?")

        if question(text) and my_recipe == None:
            if "recipe" in text:
                done, my_recipe = recipe_init()
                if done:
                    break
                # Recipe Initialization

                choice = get_input()
                processed = False
                quit = False
                while not processed:
                    if choice == "1":
                        send("The following ingredients are required by this recipe: ")
                        send_ingredients(my_recipe)
                        send("What else can I do?")
                        response = get_input()
                        if "step" in response or "procedure" in response or "2" in response:
                            choice = "2"
                        else:
                            processed = True
                    elif choice == "2":
                        quit = handle_steps(my_recipe)
                        processed = True
                    elif finish(choice):
                        quit = True
                        processed = True
                        break
                    else:
                        send("Please enter either 1 or 2 to proceed")
                        choice = get_input()
                if quit:
                    break
            else:
                send("Is this related to a recipe?")
                choice = get_input()
                if "y" in choice or "Y" in choice or "s" in choice or "S" in choice:
                    done, my_recipe = recipe_init()
                    if done:
                        break
                    # Recipe Initialization

                    choice = get_input()
                    processed = False
                    quit = False
                    while not processed:
                        if choice == "1":
                            send("The following ingredients are required by this recipe: ")
                            send_ingredients(my_recipe)
                            send("What else can I do?")
                            response = get_input()
                            if "step" in response or "procedure" in response or "2" in response:
                                choice = "2"
                            else:
                                processed = True
                        elif choice == "2":
                            quit = handle_steps(my_recipe)
                            processed = True
                        elif finish(choice):
                            quit = True
                            processed = True
                            break
                        else:
                            send("Please enter either 1 or 2 to proceed")
                            choice = get_input()
                    if quit:
                        break
                else:
                    send("I didn't get that. Please try again")

        elif len(text) > 4 and text[:4] == "http":
            try:
                my_recipe = parse_tools.recipe(text)
                send("I have processed " + my_recipe.get_title() + " for you. What can I do now")
                send("What action do you want to perform: [1] Go over ingredients list or [2] Go over recipe steps.")
            except:
                send("Sorry, the url entered does not seem to work. Please try again.")
            else:
                choice = get_input()
                processed = False
                quit = False
                while not processed:
                    if choice == "1":
                        send("The following ingredients are required by this recipe: ")
                        send_ingredients(my_recipe)
                        send("What else can I do?")
                        response = get_input()
                        if "step" in response or "procedure" in response:
                            choice = "2"
                        else:
                            processed = True
                    elif choice == "2":
                        quit = handle_steps(my_recipe)
                        processed = True
                    elif finish(choice):
                        quit = True
                        processed = True
                        break
                    else:
                        send("Please enter either 1 or 2 to proceed")
                        choice = get_input()
                if quit:
                    break

                # Recipe handling

        text = get_input()
        text = text.lower()
    send("Thank you for using Recipe Master. Have a nice day.")
    return

    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text="check"
    )

def handle_steps(rec):
    lib=rec.get_steps()
    step=0
    done=False
    quit=False
    show=True
    while step<=len(lib) and not done:
        if step==len(lib):
            send("You have reached the end of the recipe")
            send("You can [1]start from the beginning [2]process a new recipe [3]quit the program")
            ch=get_input()
            poss=["1","2","3"]
            if ch not in poss:
                send("Please enter a valid choice")
            elif ch=="1":
                step=0
                show=True
                continue
            elif ch=="2":
                break
            else:
                quit=True
                break
        if show:
            if step%10==0 and step!=10:
                send("The " +str(step+1)+"-st step is: "+lib[step]["raw"])
            elif step%10==1 and step!=11:
                send("The " +str(step+1)+"-nd step is: "+lib[step]["raw"])
            elif step%10==2 and step!=12:
                send("The " +str(step+1)+"-rd step is: "+lib[step]["raw"])
            else:
                send("The " +str(step+1)+"-th step is: "+lib[step]["raw"])
        show=True

        action=get_input()
        action=action.lower()
        if(question(action) and "ingredient" not in action):
            if ("this" in action or "that" in action) and ("how many" not in action and "how much" not in action and "how long" not in action and "when" not in action and "temperature" not in action):
                if "what" in action and "substitute" not in action and "replace" not in action:
                    if len(lib[step]["tools"])==0:
                        send("Sorry, I do not know what you are referring to.")
                    elif len(lib[step]["tools"])==1:
                        query=search_google("what is "+lib[step]["tools"][0])
                        send("I found the following results for you: "+query)
                    else:
                        send("Which one of these tools are you referring to: "+str(lib[step]["tools"]))
                        choice=get_input()
                        choice=choice.lower()
                        query=search_google("what is "+choice)
                        send("I found the following results for you: " + query)

                elif "substitute" in action or "replace" in action:
                    if len(lib[step]["ingredients"])==0:
                        send("Sorry, I do not know what you are referring to.")
                    elif len(lib[step]["ingredients"])==1:
                        query=rec.find_substitute(action)
                        if query!="not found":
                            send("I found the following result for you: "+query)
                        else:
                            send("Sorry, I cannot find a result.")
                    else:
                        send("Which one of these ingredients are you referring to: "+str(lib[step]["ingredients"]))
                        choice=get_input()
                        choice=choice.lower()
                        if choice in data.Substitution_General:
                            send("I found the following result for you: " + data.Substitution_General[choice])
                        else:
                            query = rec.find_substitute(choice)
                            if query != "not found":
                                send("I found the following result for you: " + query)
                            else:
                                send("Sorry, I cannot find a result.")


                else:
                    if len(lib[step]["methods"])==0:
                        send("Sorry, I do not know what you are referring to.")
                    elif len(lib[step]["methods"])==1:
                        query=search_youtube("how to "+lib[step]["methods"][0])
                        send("I found the following results for you: "+query)
                    else:
                        send("Which one of these actions are you referring to: "+str(lib[step]["methods"]))
                        choice=get_input()
                        choice=choice.lower()
                        query=search_youtube("how to "+choice)
                        send("I found the following results for you: " + query)

            elif "how much" in action or "how many" in action:
                kw = action.split()
                start = 0
                end = len(kw)
                for ele in range(len(kw)):
                    if kw[ele] == "much" or kw[ele] == "many":
                        if ele + 1 < len(kw) and kw[ele + 1] == "of":
                            start = ele + 2
                        else:
                            start = ele + 1
                    elif kw[ele] == "do" or (end == len(kw) and kw[ele] == "i"):
                        end = ele
                target = " ".join(kw[start:end])
                ing = rec.get_ingredients()
                if target in ing:
                    send("You need " + str(ing[target]["quantity"]) + " " + ing[target]["unit"] + " of " + target)
                else:
                    match = []
                    source = set(target.split())
                    for keys in ing:
                        for w in keys.split():
                            if w in source and keys not in ing:
                                match.append(keys)
                    if len(match) == 1:
                        send("You need " + str(ing[match[0]]["quantity"]) + " " + ing[match[0]][
                            "unit"] + " of " + target)
                    elif len(match)==0:
                        send("Sorry, we cannot find a match.")
                    else:
                        send("which one of "+str(match)+ " are you referring to?")
                        found = False
                        while not found:
                            choice = get_input()
                            choice = choice.lower()
                            if choice in match:
                                send("You need " + str(ing[match[0]]["quantity"]) + " " + ing[match[0]][
                                    "unit"] + " of " + target)
                                found = True
                            else:
                                send("Please enter a valid choice")

            elif "temperature" in action:
                if "degrees" not in lib[step]["raw"]:
                    send("Sorry, I cannot find valid temperature information")
                else:
                    sp = lib[step]["raw"].split()
                    C = ""
                    F = ""
                    for i in range(len(sp)):
                        if sp[i] == "degrees":
                            if i < len(sp) - 1 and sp[i + 1] == "f":
                                F = " ".join(sp[i - 1:i + 2])
                            elif i < len(sp) - 1 and sp[i + 1] == "c)":
                                C = " ".join(sp[i - 1:i + 2])
                    send("The temperature you need is " + F + " " + C)

            elif "how long" in action or "when" in action:
                if "time" in lib[step] and len(lib[step]["time"]) > 0:
                    send("It takes " + str(lib[step]["time"]["quantity"]) + " " + str(lib[step]["time"]["unit"]))
                else:
                    send("Sorry, the parser cannot find time information")


            else:
                if "what" in action and "substitute" not in action and "replace" not in action:
                    query = search_google(action)
                    send("I found the following results for you: " + query)
                elif "substitute" in action or "replace" in action:
                    query = rec.find_substitute(action)
                    if query != "not found":
                        send("I found the following result for you: " + query)
                    else:
                        send("Sorry, I cannot find a result.")
                else:
                    query = search_youtube(action)
                    send("I found the following results for you: " + query)




        elif "next" in action:
            step+=1

        elif "previous" in action or "go back" in action:
            if step-1<0:
                send("You are at the start of the recipe.")
            else:
                step-=1

        elif "go to" in action or "jump to" in action:
            jump=False
            while not jump:
                q = action.split()
                update = -1
                for ele in range(len(q)):
                    if q[ele]=="step":
                        try:
                            update=int(q[ele+1])
                        except:
                            send("I cannot find a valid number. Please enter a number in range [1, "+str(len(lib))+"]")
                    elif q[ele].isdigit():
                        update=int(q[ele])
                if update==-1 or update<1 or update>len(lib):
                    send("Please enter a number in range [1, " + str(len(lib)) + "]")
                    action=get_input()
                else:
                    step=update-1
                    jump=True


        elif "ingredient" in action:
            send_ingredients(rec)

        elif finish(action):
            done=True
            quit=True
        elif "thank" in action:
            send("No problem!")
        else:
            send("Sorry, I do not understand that, please try again")

        if not done and "next" not in action and "go to" not in action and "jump to" not in action and "previous" not in action:
            send("Do you want to go to the next step?")
            ac=get_input()
            ac=ac.lower()
            if "yes" in ac or "sure" in ac or "yep" in ac or "please" in ac or "ok" in ac:
                show=True
                step+=1
            elif finish(ac):
                show=False
                done=True
                quit=True
            else:
                show=True
    return quit

if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")