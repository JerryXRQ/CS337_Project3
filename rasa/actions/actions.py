# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from copyreg import dispatch_table
from typing import Any, Text, Dict, List
from rasa_sdk.events import SlotSet
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from . import parse_tools


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")

        return []

class ActionShowIngredients(Action):
    def name(self):
        return "action_showingr"
    def run(self, dispatcher, tracker, domain):
        ingred = tracker.get_slot("recipe")[2]
        #dispatcher.utter_message(text=f"{ingred}")
        dispatcher.utter_message(text="Ingredients:")        
        for i in ingred.keys():
            q = ingred[i]["quantity"]
            u = ingred[i]["unit"]
            n = i
            p = ' '.join(ingred[i]["prep"])
            dispatcher.utter_message(text=f'{q}  {u}  {n}  {p}')
        return []
        

class ActionSaveURL(Action):
    def name(self):
        return "action_saveurl"

    def run(self, dispatcher, tracker, domain):
            #tracker: Tracker,
            #domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        url1 = tracker.latest_message.get("text")
        
        dispatcher.utter_message(text=f"Processing {url1}")
        rec = parse_tools.recipe(url1)
        
        title = rec.title
        steps = rec.steps
        ingredients = rec.ingredients
        primary_method = rec.primary_method
        secondary_method = rec.secondary_method

        rec_list = [title, steps, ingredients, primary_method, secondary_method]
        dispatcher.utter_message(text=f"Got Title:  {title}")

        
        return [SlotSet("recipe", rec_list), SlotSet("url", url1), SlotSet("step", 0)] 

def show_step_n(steps, n_step):
    #return steps[n_step]["raw"]
    try:
        return steps[n_step]["raw"]
    except:
        return "reached end of recipe"


class ActionStartOver(Action):
    def name(self):
        return "action_startover"
    def run(self, dispatcher, tracker, domain):
        return [SlotSet("step", 0)]

class ActionSetStep(Action):
    def name(self):
        return "action_setstep"
    def run(self, dispatcher, tracker, domain):
        ent = int(tracker.latest_message['entities'][0]['value'])
        return [SlotSet("step", ent-1)]

class ActionShowStepForward(Action):
    def name(self):
        return "action_showstep"

    def run(self, dispatcher, tracker, domain):
        step_n = tracker.get_slot("step")
        recipe = tracker.get_slot("recipe")
        steps = recipe[1]
        #dispatcher.utter_message(text=f"{steps}")
        #estep_n = 0
        dispatcher.utter_message(text=f"Getting step: {step_n + 1}")
        curr_step = show_step_n(steps, step_n)
        #dispatcher.utter_message(text=f"{curr_step}")
        if curr_step != "reached end of recipe":
            dispatcher.utter_message(text=f"{curr_step}")
            dispatcher.utter_message(text=f"What would you like to do next? If you would like the next step, please write 'next'.")
        else:
            dispatcher.utter_message(text=f"You have reached the end of the recipe. Would you like to start over or go to a certain step [n]?")
        return[SlotSet("step", step_n+1)]
        #return[]

class ActionHowSearch(Action):
    def name(self):
        return "action_howsearch"
    def run(self, dispatcher, tracker, domain):
        question = tracker.latest_message.get("text")
        query="https://www.youtube.com/results?search_query="
        Link = query+question.replace(" ","+")
        dispatcher.utter_message(text= "YouTube Search Results: %s" % (Link))
        return []


class ActionWhatSearch(Action):
    def name(self):
        return "action_whatsearch"
    def run(self, dispatcher, tracker, domain):
        question = tracker.latest_message.get("text")
        query = "https://www.google.com/search?q="
        Link = query+question.replace(" ","+")
        dispatcher.utter_message(text= "Google Search Results: %s" % (Link))
        return []

