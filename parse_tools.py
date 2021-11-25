'''Version 0.35'''
from bs4 import BeautifulSoup
import requests
from collections import defaultdict
import data
import random
from fractions import Fraction
from math import floor
import re
import copy

class recipe():
    ingredients = {}
    primary_method = []
    secondary_method=[]
    steps=[]
    title=""


    def print_ingredients(self):
        print('\n')
        print("List of Ingredients: ")
        print('\n')
        for ele in self.ingredients.keys():
            print("Name: ", ele)
            print("Quantity: ", self.ingredients[ele]["quantity"])
            print("Unit: ", self.ingredients[ele]["unit"])
            print("Preparation: ", self.ingredients[ele]["prep"])
            print("Descriptions: ", self.ingredients[ele]["descriptions"])
            print("Additional Instruction: ", self.ingredients[ele]["additional"])
            print("\n")

        return


    def print_steps(self):
        print('\n')
        print("List of Steps: ")
        print('\n')
        counter=1
        for ele in self.steps:
            for e in ele.keys():
                print("Step ",counter,e,": ",ele[e])
            print("\n")
            counter+=1


    def print_methods(self):
        if len(self.primary_method)>0:
            print("Primary Method: ",self.primary_method[0])
        else:
            print("We cannot find any matching primary methods")
        if len(self.secondary_method)>0:
            print("Secondary Method: ", self.secondary_method[:min(len(self.secondary_method), 3)])
        else:
            print("We cannot find any matching secondary methods")


    def process_ingredients(self,ele):
        #print(ele)
        temp=ele.replace(",","")
        temp=temp.replace(" ¼",".25")
        temp = temp.replace("¼", ".25")
        temp=temp.replace(" ¾",".75")
        temp = temp.replace("¾", ".75")
        temp=temp.replace(" ½",".5")
        temp = temp.replace("½", ".5")
        temp=temp.replace(" ⅓",".33")
        temp = temp.replace("⅓", ".33")
        temp = temp.replace("⅐",".143")
        temp = temp.replace("⅜",".375")
        temp = temp.replace("⅖",".4")
        temp = temp.replace("⅔",".66")
        temp = temp.replace("- ", "")
        temp=temp.replace("-inch"," inch")
        temp=temp.replace(" or more","")
        temp = temp.replace(" or to taste", "")
        dic={}
        #ele.replace()
        prep_result=set(["into","to"])
        words=temp.split()
        quantity=0
        unit=""
        name=""
        additional=[]
        prep=[]
        descriptions=[]
        #print(words)
        e=0
        while e < len(words):
            if words[e][0]=="(":
                desc=words[e][1:]
                if ")" in words[e]:
                    desc.replace(")","")
                    temp = temp.replace(words[e], "")
                    temp = temp.replace("  ", " ")
                    break
                else:
                    temp = temp.replace(words[e], "")
                    temp = temp.replace("  ", " ")
                e+=1
                while e<len(words) and words[e][-1]!=")":
                    temp=temp.replace(words[e],"")
                    temp=temp.replace("  "," ")
                    desc+=" "+words[e]
                    e+=1
                temp = temp.replace(words[e], "")
                temp = temp.replace("  ", " ")
                desc+=words[e][:len(words[e])-1]
            e+=1
        update=temp.split()
        #print(update)
        found=False
        if update[0][0] in set([".", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]) and update[1] not in data.Liquid_Measurements and update[1] not in data.Solid_Measurements:
            quantity = float(words[0])
            unit = "Count"
            name = " ".join(update[1:])
            found=True
        for w in range(len(update)):
            if update[w] in data.Liquid_Measurements or update[w] in data.Solid_Measurements:
                if w>0 and not found:
                    try:
                        quantity=float(update[w-1])
                        unit=update[w]
                        name=" ".join(update[w+1:])
                        found=True
                    except:
                        try:
                            q = float(Fraction(update[w - 1]))
                            unit=update[w]
                            name=" ".join(update[w+1:])
                            found=True
                        except:
                            found=False
                elif w>0:
                    try:

                        q=float(update[w-1])
                        unit=update[w]
                        name = name.replace(update[w], "")
                        name = name.replace(update[w - 1], "")
                        name = name.replace("  ", "")
                        additional.append(str(q)+" "+unit)
                    except:
                        try:
                            q = float(Fraction(update[w - 1]))
                            add = str(q)+" "+update[w]
                            additional.append(add)
                            name=name.replace(update[w],"")
                            name=name.replace(update[w-1],"")
                            name=name.replace("  ","")
                        except:
                            continue
        if not found:
                quantity=0
                name=" ".join(update)
                unit="Based on Preference"
        split=name.split()
        for index in range(len(split)):
            if split[index] in data.prep:
                name=name.replace(split[index],"")
                name=name.replace("  "," ")
                if index+1<len(split) and split[index+1]in prep_result:
                    name=name.replace(split[index+1],"")
                    name=name.replace("  "," ")
                prep.append(split[index])

            for types in data.descriptors.keys():
                if split[index] in data.descriptors[types]:
                    name = name.replace(split[index], "")
                    name = name.replace("  ", " ")
                    descriptions.append(split[index])
        if len(name)==0:
            return None
        if name[0]==" ":
            name=name[1:]
        if len(name)==0:
            return None
        if name[len(name)-1]==" ":
            name=name[:len(name)-1]
        name=name.replace("for","")
        name=name.replace("  "," ")
        name = name.replace(" or", "")
        name = name.replace(" and","")
        name = name.replace("and ", "")
        name=name.replace(" as needed","")
        name = name.replace("as needed", "")
        name=name.replace(" to taste","")
        dic["quantity"]=quantity
        dic["unit"]=unit
        dic["name"]=name.lower()
        dic["prep"]=prep
        dic["descriptions"]=descriptions
        dic["additional"]=additional

        return dic


    def process_methods_primary(self,step):
        counter=defaultdict(int)
        temp=step.lower()
        for ele in temp.split():
            if ele in data.Method_Primary:
                counter[ele]+=1
        for k in data.Tools_to_Method:
            if k in temp:
                counter[data.Tools_to_Method[k]]+=1
        return counter


    def process_methods_secondary(self,step):
        counter=defaultdict(int)
        temp=step.lower()
        for ele in temp.split():
            if ele in data.Method_Secondary:
                counter[ele]+=1
        return counter


    def process_steps(self,step):
        target=step.lower()
        steps=[]
        sentences=target.split(".")

        #print(sentences)
        for sentence in sentences:
            sentence=sentence.replace(" 1/2",".5")
            sentence=sentence.replace("1/2", ".5")
            sentence=sentence.replace(" 1/4",".25")
            sentence=sentence.replace("1/4", ".25")
            sentence = sentence.replace(" 3/4", ".75")
            sentence = sentence.replace("3/4", ".75")
            sentence=sentence.replace(",","")
            sentence=sentence.replace(";","")
            dic={}
            temp={}
            for st in ["   step 1   ","   step 2   ","   step 3   ","   step 4   ","   step 5   ","   step 6   ","   step 7   ","   step 8   ","   step 9   ","   step 10   ","   step 11   ","   step 12   ","   step 13   ","   step 14   ","   step 15   "]:
                sentence=sentence.replace(st,"")
            dic["raw"] = sentence
            lis=sentence.split()
            for ele in range(len(lis)):
                if lis[ele] in data.Time_Units:
                    temp["unit"]=lis[ele]
                    try:
                        temp["quantity"]=float(lis[ele-1])
                    except:
                        temp["quantity"]=1
            dic["time"]=temp
            #Update Time in the step

            dic["tools"]=[]
            for items in data.Tools:
                if items in sentence:
                    dic["tools"].append(items)
            #Update Tools used

            dic["methods"]=[]
            for items in data.Method_Primary:
                if items in sentence:
                    dic["methods"].append(items)

            for items in data.Method_Secondary:
                if items in sentence and items not in dic["methods"]:
                    dic["methods"].append(items)

            dic["ingredients"]=[]
            for ele in self.ingredients:
                if ele in sentence and ele not in dic["ingredients"]:
                    dic["ingredients"].append(ele)
                elif ele[-1]=="s" and ele[:len(ele)-1] in sentence and ele[:len(ele)-1] not in dic["ingredients"]:
                    dic["ingredients"].append(ele)
                else:
                    for kw in ele.split():
                        if kw in sentence and kw not in dic["ingredients"]:
                            dic["ingredients"].append(kw)
                        elif kw[-1]=="s" and kw[:len(kw)-1] in sentence:
                            dic["ingredients"].append(kw)
            for ele in data.Meat_Parts:
                if ele in sentence and ele not in dic["ingredients"] and ele not in " ".join(dic["ingredients"]):
                    dic["ingredients"].append(ele)
            if len(dic["ingredients"])>0 or len(dic["methods"])>0 or len(dic["tools"])>0 or len(dic["time"])>0:
                steps.append(dic)
        return steps

    def process_methods_bs(self,res):
        found=False
        for me in data.Method_Primary:
            if me in self.title:
                self.primary_method.append(me)
                found=True
        if not found:
            pm = defaultdict(int)
            for ele in res:
                s = self.process_methods_primary(ele.get_text())
                for keys in s:
                    pm[keys] += s[keys]
            self.primary_method = [k for k in pm.keys()]
            self.primary_method.sort(key=lambda x: pm[x], reverse=True)
        # Find Primary Method

        sm = defaultdict(int)
        for ele in res:
            t = self.process_methods_secondary(ele.get_text())
            for keys in t:
                sm[keys] += t[keys]
        self.secondary_method = [k for k in sm.keys()]
        self.secondary_method.sort(key=lambda x: sm[x], reverse=True)
        #Find Secondary Method

    def process_methods(self,res):
        pm = defaultdict(int)
        for ele in res:
            s = self.process_methods_primary(ele["raw"])
            for keys in s:
                pm[keys] += s[keys]
        #print(pm)
        self.primary_method = [k for k in pm.keys()]
        self.primary_method.sort(key=lambda x: pm[x], reverse=True)
        # Find Primary Method

        sm = defaultdict(int)
        for ele in res:
            t = self.process_methods_secondary(ele["raw"])
            for keys in t:
                sm[keys] += t[keys]
        self.secondary_method = [k for k in sm.keys()]
        self.secondary_method.sort(key=lambda x: sm[x], reverse=True)
        #Find Secondary Method


    def to_Vegetarian(self):
        replaced=[]
        replacement=[]
        match={}
        for ele in self.ingredients.keys():
            meat=False
            for words in ele.split():
                if words in data.Non_Vegan["meat"]:
                    meat=True
                    break
            if meat:
                replaced.append(ele)
                find=random.sample(data.Vegan_Protein,1)
                while find[0] in replacement and len(replacement)<len(data.Vegan_Protein):
                    find=random.sample(data.Vegan_Protein,1)
                replacement.append(find[0])
                for sw in ele.split():
                    match[sw]=find[0]
        if len(replaced) == 0:
            print("Sorry, we fail to find a replacement. This recipe is already vegetarian.")
            return True
        else:
            print("We found the following items that need to be replaced: ", replaced)
            print("We replaced them with: ", replacement)
        for ele in range(len(replaced)):
            dic={}
            dic["name"]=replacement[ele]
            dic["quantity"]=self.ingredients[replaced[ele]]["quantity"]
            dic["unit"]=self.ingredients[replaced[ele]]["unit"]
            dic["prep"] = self.ingredients[replaced[ele]]["prep"]
            dic["descriptions"] = []
            dic['unit_type']=self.ingredients[replaced[ele]]['unit_type']

            for w in self.ingredients[replaced[ele]]["descriptions"]:
                if w not in data.descriptors["meat"]:
                    dic["descriptions"].append(w)

            dic["additional"] = self.ingredients[replaced[ele]]["additional"]
            if replacement[ele] in self.ingredients:
                self.ingredients.pop(replaced[ele])
                if self.ingredients[replacement[ele]]["unit"] == dic["unit"]:
                    self.ingredients[replacement[ele]]["quantity"] += dic["quantity"]
                else:
                    u = []
                    q = []
                    u.append(self.ingredients[replacement[ele]]["unit"])
                    u.append(dic["unit"])
                    q.append(self.ingredients[replacement[ele]]["quantity"])
                    q.append(dic["quantity"])
                    self.ingredients[replacement[ele]]["quantity"] = q
                    self.ingredients[replacement[ele]]["unit"] = u
                    self.ingredients[replacement[ele]]["descriptions"] += dic["descriptions"]
                    self.ingredients[replacement[ele]]["prep"] += dic["prep"]

            else:
                self.ingredients.pop(replaced[ele])
                self.ingredients[replacement[ele]] = dic

        for i in range(len(self.steps)):
            new_lis = []
            for ele in replaced:
                if ele in self.steps[i]["raw"]:
                    self.steps[i]["raw"] = self.steps[i]["raw"].replace(ele, replacement[replaced.index(ele)])
                elif ele[-1] == "s" and ele[:len(ele) - 1] in self.steps[i]["raw"]:
                    self.steps[i]["raw"] = self.steps[i]["raw"].replace(ele[:len(ele) - 1],
                                                                        replacement[replaced.index(ele)])

            sp = self.steps[i]["raw"].split()
            for ele in sp:
                if ele in data.descriptors["meat"] or ele in data.descriptors["dairy"]:
                    self.steps[i]["raw"] = self.steps[i]["raw"].replace(ele, "")
                    self.steps[i]["raw"] = self.steps[i]["raw"].replace("  ", "")
                elif ele in data.Meat_Parts:
                    chos = random.choice(replacement)
                    self.steps[i]["raw"] = self.steps[i]["raw"].replace(ele, chos)
                elif ele in match:
                    self.steps[i]["raw"] = self.steps[i]["raw"].replace(ele, match[ele])

            sentence = self.steps[i]["raw"]
            for ele in self.ingredients:
                if ele in sentence and ele not in new_lis:
                    new_lis.append(ele)
                elif ele[-1] == "s" and ele[:len(ele) - 1] in sentence and ele[:len(ele) - 1] not in new_lis:
                    new_lis.append(ele)
                else:
                    for kw in ele.split():
                        if kw in sentence and kw not in new_lis:
                            new_lis.append(kw)
                        elif kw[-1] == "s" and kw[:len(kw) - 1] in sentence and kw not in new_lis:
                            new_lis.append(kw)
            self.steps[i]["ingredients"] = new_lis

        return True

    def to_Vegan(self):
        replaced = []
        replacement = []
        replaced_m=[]
        replacement_m=[]
        match={}
        for ele in self.ingredients.keys():
            meat = False
            for words in ele.split():
                if words in data.Non_Vegan["meat"]:
                    meat = True
                    break
            if meat:
                replaced.append(ele)
                replaced_m.append(ele)
                find = random.sample(data.Vegan_Protein, 1)
                while find[0] in replacement and len(replacement) < len(data.Vegan_Protein):
                    find = random.sample(data.Vegan_Protein, 1)
                replacement.append(find[0])
                replacement_m.append(find[0])
                for sw in ele.split():
                    match[sw]=find[0]
        for ele in self.ingredients.keys():
            if ele in data.Vegan:
                replaced.append(ele)
                replacement.append(data.Vegan[ele])
            else:
                for words in ele.split():
                    if words in data.Vegan and ele not in replaced:
                        replaced.append(ele)
                        replacement.append(data.Vegan[words])
        if len(replaced) == 0:
            print("Sorry, we fail to find a replacement. This recipe is already vegan.")
            return True
        else:
            print("We found the following items that need to be replaced: ", replaced)
            print("We replaced them with: ", replacement)
        for ele in range(len(replaced)):
            dic={}
            dic["name"]=replacement[ele]
            dic["quantity"]=self.ingredients[replaced[ele]]["quantity"]
            dic["unit"]=self.ingredients[replaced[ele]]["unit"]
            dic["prep"] = self.ingredients[replaced[ele]]["prep"]
            dic["descriptions"] = []
            dic['unit_type']=self.ingredients[replaced[ele]]['unit_type']

            #print(self.ingredients[replaced[ele]])
            for w in self.ingredients[replaced[ele]]["descriptions"]:
                if w not in data.descriptors["meat"] and w not in data.descriptors["dairy"]:
                    dic["descriptions"].append(w)

            dic["additional"] = self.ingredients[replaced[ele]]["additional"]
            if replacement[ele] in self.ingredients:
                self.ingredients.pop(replaced[ele])
                if self.ingredients[replacement[ele]]["unit"] == dic["unit"]:
                    self.ingredients[replacement[ele]]["quantity"] += dic["quantity"]
                else:
                    u = []
                    q = []
                    u.append(self.ingredients[replacement[ele]]["unit"])
                    u.append(dic["unit"])
                    q.append(self.ingredients[replacement[ele]]["quantity"])
                    q.append(dic["quantity"])
                    self.ingredients[replacement[ele]]["quantity"] = q
                    self.ingredients[replacement[ele]]["unit"] = u
                    self.ingredients[replacement[ele]]["descriptions"] += dic["descriptions"]
                    self.ingredients[replacement[ele]]["prep"] += dic["prep"]

            else:
                self.ingredients.pop(replaced[ele])
                self.ingredients[replacement[ele]] = dic


        for i in range(len(self.steps)):
            new_lis=[]
            for ele in replaced:
                if ele in self.steps[i]["raw"]:
                    self.steps[i]["raw"] = self.steps[i]["raw"].replace(ele, replacement[replaced.index(ele)])
                elif ele[-1]=="s" and ele[:len(ele)-1] in self.steps[i]["raw"]:
                    self.steps[i]["raw"] = self.steps[i]["raw"].replace(ele[:len(ele)-1], replacement[replaced.index(ele)])

            sp = self.steps[i]["raw"].split()
            for ele in sp:
                if ele in data.descriptors["meat"] or ele in data.descriptors["dairy"]:
                    self.steps[i]["raw"] = self.steps[i]["raw"].replace(ele, "")
                    self.steps[i]["raw"] = self.steps[i]["raw"].replace("  ", " ")
                elif ele in data.Meat_Parts and len(replacement_m)>0:
                    chos = random.choice(replacement_m)
                    self.steps[i]["raw"] = self.steps[i]["raw"].replace(ele, chos)
                elif ele in match:
                    self.steps[i]["raw"] = self.steps[i]["raw"].replace(ele, match[ele])

            sentence=self.steps[i]["raw"]
            for ele in self.ingredients:
                if ele in sentence and ele not in new_lis:
                    new_lis.append(ele)
                elif ele[-1] == "s" and ele[:len(ele) - 1] in sentence and ele[:len(ele) - 1] not in new_lis:
                    new_lis.append(ele)
                else:
                    for kw in ele.split():
                        if kw in sentence and kw not in new_lis:
                            new_lis.append(kw)
                        elif kw[-1] == "s" and kw[:len(kw) - 1] in sentence:
                            new_lis.append(kw)
            self.steps[i]["ingredients"]=new_lis


        return True


    def to_Non_Vegetarian(self):
        replaced=[]
        replacement=[]
        for ele in self.ingredients.keys():
            vege=False
            for words in ele.split():
                if words in data.Vegetable and "oil" not in ele:
                    vege=True
                    break
            if vege:
                replaced.append(ele)
                find=random.sample(data.Non_Vegan["meat"],1)
                while find[0] in replacement and len(replacement)<len(data.Non_Vegan["meat"]):
                    find=random.sample(data.Non_Vegan["meat"],1)
                replacement.append(find[0])
        if len(replaced)==0:
            print("Sorry, we fail to find a replacement. This recipe is already non-vegetarian.")
            return False
        else:
            print("We found the following items that need to be replaced: ",replaced)
            print("We replaced them with: ",replacement)

        for ele in range(len(replaced)):
            dic={}
            dic["name"]=replacement[ele]
            dic["quantity"]=self.ingredients[replaced[ele]]["quantity"]
            dic["unit"]=self.ingredients[replaced[ele]]["unit"]
            dic["prep"] = self.ingredients[replaced[ele]]["prep"]
            dic["descriptions"] = []
            dic['unit_type']=self.ingredients[replaced[ele]]['unit_type']
            for w in self.ingredients[replaced[ele]]["descriptions"]:
                if w not in data.descriptors["veggie"]:
                    dic["descriptions"].append(w)

            dic["additional"] = self.ingredients[replaced[ele]]["additional"]
            if replacement[ele] in self.ingredients:
                self.ingredients.pop(replaced[ele])
                if self.ingredients[replacement[ele]]["unit"] == dic["unit"]:
                    self.ingredients[replacement[ele]]["quantity"] += dic["quantity"]
                else:
                    u = []
                    q = []
                    u.append(self.ingredients[replacement[ele]]["unit"])
                    u.append(dic["unit"])
                    q.append(self.ingredients[replacement[ele]]["quantity"])
                    q.append(dic["quantity"])
                    self.ingredients[replacement[ele]]["quantity"] = q
                    self.ingredients[replacement[ele]]["unit"] = u
                    self.ingredients[replacement[ele]]["descriptions"] += dic["descriptions"]
                    self.ingredients[replacement[ele]]["prep"] += dic["prep"]

            else:
                self.ingredients.pop(replaced[ele])
                self.ingredients[replacement[ele]] = dic

        for i in range(len(self.steps)):
            new_lis = []
            for ing in self.steps[i]["ingredients"]:
                if ing in replaced:
                    new_lis.append(replacement[replaced.index(ing)])
                else:
                    new_lis.append(ing)
            sp=self.steps[i]["raw"].split()
            for ele in sp:
                if ele in replaced:
                    self.steps[i]["raw"]=self.steps[i]["raw"].replace(ele,replacement[replaced.index(ele)])
                elif ele in data.descriptors["veggie"]:
                    self.steps[i]["raw"]=self.steps[i]["raw"].replace(ele,"")
                    self.steps[i]["raw"] = self.steps[i]["raw"].replace("  ", "")


            self.steps[i]["ingredients"] = new_lis
        return True

    def to_Healty(self):
        replaced = []
        replacement = []
        det=False
        present=defaultdict(list)
        match={}
        for ele in self.ingredients.keys():
            if ele in data.Make_Healthy["ingredients"]:
                replaced.append(ele)
                replacement.append(data.Make_Healthy["ingredients"][ele])
                present["Ingredient Change: "].append([replaced[-1],replacement[-1]])
                det=True
                for subw in ele.split():
                    match[subw]=replacement[-1]
        for i in range(len(self.steps)):
            for app in self.steps[i]["methods"]:
                if app in data.Make_Healthy["approach"]:
                    present["Method Change: "].append([app, data.Make_Healthy["approach"][app]])
                    det=True
            for app in self.steps[i]["tools"]:
                if app in data.Make_Healthy["tools"]:
                    present["Tool Change: "].append([app, data.Make_Healthy["tools"][app]])
                    det=True
        if not det:
            print("Sorry, we cannot find any transformations that can make this recipe healthier")
            return False
        else:
            print("We found the following substitutions: ")
            for keys in present:
                print(keys,present[keys])

        for ele in range(len(replaced)):
            dic={}
            dic["name"]=replacement[ele]
            dic["quantity"]=self.ingredients[replaced[ele]]["quantity"]
            dic["unit"]=self.ingredients[replaced[ele]]["unit"]
            dic["prep"] = self.ingredients[replaced[ele]]["prep"]
            dic["descriptions"] = self.ingredients[replaced[ele]]["descriptions"]
            dic["additional"] = self.ingredients[replaced[ele]]["additional"]
            dic["unit_type"]=self.ingredients[replaced[ele]]["unit_type"]
            if replacement[ele] in self.ingredients:
                self.ingredients.pop(replaced[ele])
                if self.ingredients[replacement[ele]]["unit"]==dic["unit"]:
                    self.ingredients[replacement[ele]]["quantity"]+=dic["quantity"]
                else:
                    u = []
                    q = []
                    u.append(self.ingredients[replacement[ele]]["unit"])
                    u.append(dic["unit"])
                    q.append(self.ingredients[replacement[ele]]["quantity"])
                    q.append(dic["quantity"])
                    self.ingredients[replacement[ele]]["quantity"] = q
                    self.ingredients[replacement[ele]]["unit"] = u
                    self.ingredients[replacement[ele]]["descriptions"] += dic["descriptions"]
                    self.ingredients[replacement[ele]]["prep"] += dic["prep"]

            else:
                self.ingredients.pop(replaced[ele])
                self.ingredients[replacement[ele]]=dic

        for i in range(len(self.steps)):
            new_lis_ing = []
            new_lis_app=[]
            new_lis_tools=[]
            for ing in self.steps[i]["ingredients"]:
                if ing in replaced:
                    new_lis_ing.append(replacement[replaced.index(ing)])
                    self.steps[i]["raw"]=self.steps[i]["raw"].replace(ing, replacement[replaced.index(ing)])
                elif ing in match and match[ing] not in self.steps[i]["raw"]:
                    new_lis_ing.append(match[ing])
                    self.steps[i]["raw"] = self.steps[i]["raw"].replace(ing, match[ing])
                else:
                    new_lis_ing.append(ing)
            self.steps[i]["ingredients"] = new_lis_ing


            for app in self.steps[i]["methods"]:
                if app in data.Make_Healthy["approach"]:
                    new_lis_app.append(data.Make_Healthy["approach"][app])
                    self.steps[i]["raw"]=self.steps[i]["raw"].replace(app,data.Make_Healthy["approach"][app])
                else:
                    new_lis_app.append(app)

            self.steps[i]["methods"] = new_lis_app

            for app in self.steps[i]["tools"]:
                if app in data.Make_Healthy["tools"]:
                    new_lis_tools.append(data.Make_Healthy["tools"][app])
                    self.steps[i]["raw"]=self.steps[i]["raw"].replace(app, data.Make_Healthy["tools"][app])
                else:
                    new_lis_tools.append(app)
            self.steps[i]["tools"] = new_lis_tools
        self.process_methods(self.steps)
        return True

    def to_Unhealthy(self):
        replaced = []
        replacement = []
        det = False
        present = defaultdict(list)
        for ele in self.ingredients.keys():
            if ele in data.Make_Unhealthy["ingredients"]:
                replaced.append(ele)
                replacement.append(data.Make_Unhealthy["ingredients"][ele])
                present["Ingredient Change: "].append([replaced[-1], replacement[-1]])
                det = True
        for i in range(len(self.steps)):
            for app in self.steps[i]["methods"]:
                if app in data.Make_Unhealthy["approach"]:
                    present["Method Change: "].append([app, data.Make_Unhealthy["approach"][app]])
                    det = True
            for app in self.steps[i]["tools"]:
                if app in data.Make_Unhealthy["tools"]:
                    present["Tool Change: "].append([app, data.Make_Unhealthy["tools"][app]])
                    det = True
        if not det:
            print("Sorry, we cannot find any transformations that can make this recipe more unhealthy")
            return False
        else:
            print("We found the following substitutions: ")
            for keys in present:
                print(keys, present[keys])

        for ele in range(len(replaced)):
            dic={}
            dic["name"]=replacement[ele]
            dic["quantity"]=self.ingredients[replaced[ele]]["quantity"]
            dic["unit"]=self.ingredients[replaced[ele]]["unit"]
            dic["prep"] = self.ingredients[replaced[ele]]["prep"]
            dic["descriptions"] = self.ingredients[replaced[ele]]["descriptions"]
            dic["additional"] = self.ingredients[replaced[ele]]["additional"]
            dic["unit_type"] = self.ingredients[replaced[ele]]["unit_type"]
            if replacement[ele] in self.ingredients:
                self.ingredients.pop(replaced[ele])
                if self.ingredients[replacement[ele]]["unit"] == dic["unit"]:
                    self.ingredients[replacement[ele]]["quantity"] += dic["quantity"]
                else:
                    u = []
                    q = []
                    u.append(self.ingredients[replacement[ele]]["unit"])
                    u.append(dic["unit"])
                    q.append(self.ingredients[replacement[ele]]["quantity"])
                    q.append(dic["quantity"])
                    self.ingredients[replacement[ele]]["quantity"] = q
                    self.ingredients[replacement[ele]]["unit"] = u
                    self.ingredients[replacement[ele]]["descriptions"] += dic["descriptions"]
                    self.ingredients[replacement[ele]]["prep"] += dic["prep"]

            else:
                self.ingredients.pop(replaced[ele])
                self.ingredients[replacement[ele]] = dic

        for i in range(len(self.steps)):
            new_lis_ing = []
            new_lis_app=[]
            new_lis_tools=[]
            for ing in self.steps[i]["ingredients"]:
                if ing in replaced:
                    new_lis_ing.append(replacement[replaced.index(ing)])
                    self.steps[i]["raw"] = self.steps[i]["raw"].replace(ing, replacement[replaced.index(ing)])
                else:
                    new_lis_ing.append(ing)
            self.steps[i]["ingredients"] = new_lis_ing


            for app in self.steps[i]["methods"]:
                if app in data.Make_Unhealthy["approach"]:
                    new_lis_app.append(data.Make_Unhealthy["approach"][app])
                    self.steps[i]["raw"] = self.steps[i]["raw"].replace(app, data.Make_Unhealthy["approach"][app])
                else:
                    new_lis_app.append(app)
            self.steps[i]["methods"] = new_lis_app

            for app in self.steps[i]["tools"]:
                if app in data.Make_Unhealthy["tools"]:
                    new_lis_tools.append(data.Make_Unhealthy["tools"][app])
                    self.steps[i]["raw"] = self.steps[i]["raw"].replace(app, data.Make_Unhealthy["tools"][app])
                else:
                    new_lis_tools.append(app)
            self.steps[i]["tools"] = new_lis_tools
        self.process_methods(self.steps)
        return True


    def scale(self,ratio):
        for ele in self.ingredients.keys():
            if isinstance(self.ingredients[ele]["quantity"], int) or isinstance(self.ingredients[ele]["quantity"], float):
                self.ingredients[ele]["quantity"]*=ratio
            else:
                for val in range(len(self.ingredients[ele]["quantity"])):
                    self.ingredients[ele]["quantity"][val]*=2

        for ele in range(len(self.steps)):
            if len(self.steps[ele]["time"])==2:
                num=self.steps[ele]["time"]["quantity"]
                num*=ratio**0.5
                num=floor(num)
                self.steps[ele]["time"]["quantity"]=num

            s=self.steps[ele]["raw"].split()
            #print(s)
            change_pos=[]
            for pos in range(len(s)):
                if len(self.steps[ele]["time"])>0 and s[pos] in self.steps[ele]["time"]["unit"]:
                    #print(s,ele)
                    try:
                        change_pos.append([pos-1,floor(float(s[pos-1])*ratio**0.5)])
                        if pos>=3 and s[pos-2]=="to":
                            change_pos.append([pos-3,floor(float(s[pos-3])*ratio**0.5)])
                    except:
                        continue
                elif s[pos] in data.Liquid_Measurements or s[pos] in data.Solid_Measurements:
                    try:
                        change_pos.append([pos - 1, float(s[pos - 1]) * ratio])
                    except:
                        continue
            for pair in change_pos:
                s[pair[0]]=str(pair[1])
            self.steps[ele]["raw"]=" ".join(s)

    def weight(self):
        update = []
        for ele in self.ingredients.keys():
            #print(self.ingredients[ele]["unit_type"])
            if self.ingredients[ele]["unit_type"] == "volumetric":
                self.ingredients[ele]["quantity"] = float(self.ingredients[ele]["quantity"]) * data.volume_to_gram[self.ingredients[ele]["unit"]]
                self.ingredients[ele]["unit_type"] = "weight"
                self.ingredients[ele]["unit"] = "grams"
                update.append(ele)
                #print(self.ingredients[ele])
        print("Replaced volumetric measurement with gram weights for ", update)


    def kosher(self):
        replaced = []
        replacement = []
        det = False
        present = defaultdict(list)
        meat = 0
        for ele in self.ingredients.keys():
            if ele in data.Kosher:
                replaced.append(ele)
                replacement.append(data.Kosher[ele])
                present["Ingredient Change: "].append([replaced[-1], replacement[-1]])
                det = True
            if ele in data.shellfish:
                replaced.append(ele)
                replacement.append(data.shellfish[ele])
                present["Ingredient Change: "].append([replaced[-1], replacement[-1]])
                det = True
            for i in ele.split(" "):
                if ele in data.meat:
                    meat += 1
        
        if meat != 0:
            for ele in self.ingredients.keys():
                #print(ele)
                for i in ele.split(" "):
                    if i in data.Lactose_Free.keys():
                        print(i)
                        det=True
                        replaced.append(ele)
                        replacement.append(data.Lactose_Free[i])
                        present["Ingredient Change: "].append([replaced[-1], replacement[-1]])

         
        if not det:
            print("Sorry, we cannot find any transformation. This recipe is already kosher")
            return False
        else:
            print("We found the following substitutions: ")
            for keys in present:
                print(keys, present[keys])

        for ele in range(len(replaced)):
            dic = {}
            dic["name"] = replacement[ele]
            dic["quantity"] = self.ingredients[replaced[ele]]["quantity"]
            dic["unit"] = self.ingredients[replaced[ele]]["unit"]
            dic["prep"] = self.ingredients[replaced[ele]]["prep"]
            dic["descriptions"] = self.ingredients[replaced[ele]]["descriptions"]
            dic["additional"] = self.ingredients[replaced[ele]]["additional"]
            dic["unit_type"] = self.ingredients[replaced[ele]]["unit_type"]
            if replacement[ele] in self.ingredients:
                self.ingredients.pop(replaced[ele])
                if self.ingredients[replacement[ele]]["unit"] == dic["unit"]:
                    self.ingredients[replacement[ele]]["quantity"] += dic["quantity"]
                else:
                    u = []
                    q = []
                    u.append(self.ingredients[replacement[ele]]["unit"])
                    u.append(dic["unit"])
                    q.append(self.ingredients[replacement[ele]]["quantity"])
                    q.append(dic["quantity"])
                    self.ingredients[replacement[ele]]["quantity"] = q
                    self.ingredients[replacement[ele]]["unit"] = u
                    self.ingredients[replacement[ele]]["descriptions"] += dic["descriptions"]
                    self.ingredients[replacement[ele]]["prep"] += dic["prep"]

            else:
                self.ingredients.pop(replaced[ele])
                self.ingredients[replacement[ele]] = dic

        for i in range(len(self.steps)):
            new_lis_ing = []
            for ing in self.steps[i]["ingredients"]:
                if ing in replaced:
                    new_lis_ing.append(replacement[replaced.index(ing)])
                    self.steps[i]["raw"] = self.steps[i]["raw"].replace(ing, replacement[replaced.index(ing)])
                else:
                    new_lis_ing.append(ing)
            self.steps[i]["ingredients"] = new_lis_ing
        return True

    def gluten_free(self):
        replaced = []
        replacement = []
        det = False
        present = defaultdict(list)
        for ele in self.ingredients.keys():
            if ele in data.Gluten_Free:
                replaced.append(ele)
                replacement.append(data.Gluten_Free[ele])
                present["Ingredient Change: "].append([replaced[-1], replacement[-1]])
                det = True
            elif "pasta" in ele or "macaroni" in ele:
                replaced.append(ele)
                replacement.append("spaghetti squash")
                present["Ingredient Change: "].append([replaced[-1], replacement[-1]])
                det = True

        if not det:
            print("Sorry, we cannot find any transformation. This recipe is already gluten free")
            return False
        else:
            print("We found the following substitutions: ")
            for keys in present:
                print(keys, present[keys])

        for ele in range(len(replaced)):
            dic = {}
            dic["name"] = replacement[ele]
            dic["quantity"] = self.ingredients[replaced[ele]]["quantity"]
            dic["unit"] = self.ingredients[replaced[ele]]["unit"]
            dic["prep"] = self.ingredients[replaced[ele]]["prep"]
            dic["descriptions"] = self.ingredients[replaced[ele]]["descriptions"]
            dic["additional"] = self.ingredients[replaced[ele]]["additional"]
            dic["unit_type"] = self.ingredients[replaced[ele]]["unit_type"]
            if replacement[ele] in self.ingredients:
                self.ingredients.pop(replaced[ele])
                if self.ingredients[replacement[ele]]["unit"] == dic["unit"]:
                    self.ingredients[replacement[ele]]["quantity"] += dic["quantity"]
                else:
                    u = []
                    q = []
                    u.append(self.ingredients[replacement[ele]]["unit"])
                    u.append(dic["unit"])
                    q.append(self.ingredients[replacement[ele]]["quantity"])
                    q.append(dic["quantity"])
                    self.ingredients[replacement[ele]]["quantity"] = q
                    self.ingredients[replacement[ele]]["unit"] = u
                    self.ingredients[replacement[ele]]["descriptions"] += dic["descriptions"]
                    self.ingredients[replacement[ele]]["prep"] += dic["prep"]

            else:
                self.ingredients.pop(replaced[ele])
                self.ingredients[replacement[ele]] = dic

        for i in range(len(self.steps)):
            new_lis_ing = []
            for ing in self.steps[i]["ingredients"]:
                if ing in replaced:
                    new_lis_ing.append(replacement[replaced.index(ing)])
                    self.steps[i]["raw"] = self.steps[i]["raw"].replace(ing, replacement[replaced.index(ing)])
                elif ing=="pasta" or ing=="macaroni":
                    new_lis_ing.append("spaghetti squash")
                    self.steps[i]["raw"] = self.steps[i]["raw"].replace(ing, "spaghetti squash")
                else:
                    new_lis_ing.append(ing)
            self.steps[i]["ingredients"] = new_lis_ing
        return True


    def chinese(self):
        replaced = []
        replacement = []
        det = False
        present = defaultdict(list)
        for ele in self.ingredients.keys():
            if ele in data.Chinese["ingredients"]:
                replaced.append(ele)
                replacement.append(data.Chinese["ingredients"][ele])
                present["Ingredient Change: "].append([replaced[-1], replacement[-1]])
                det = True
        for i in range(len(self.steps)):
            for app in self.steps[i]["methods"]:
                if app in data.Chinese["approach"]:
                    present["Method Change: "].append([app, data.Chinese["approach"][app]])
                    det = True
            for app in self.steps[i]["tools"]:
                if app in data.Chinese["tools"]:
                    present["Tool Change: "].append([app, data.Chinese["tools"][app]])
                    det = True
        if not det:
            print("Sorry, we cannot find any transformations. This particular recipe could not be made in Chinese style.")
            return False
        else:
            print("We found the following substitutions: ")
            for keys in present:
                print(keys, present[keys])

        for ele in range(len(replaced)):
            dic = {}
            dic["name"] = replacement[ele]
            dic["quantity"] = self.ingredients[replaced[ele]]["quantity"]
            dic["unit"] = self.ingredients[replaced[ele]]["unit"]
            dic["prep"] = self.ingredients[replaced[ele]]["prep"]
            dic["descriptions"] = self.ingredients[replaced[ele]]["descriptions"]
            dic["additional"] = self.ingredients[replaced[ele]]["additional"]
            dic["unit_type"] = self.ingredients[replaced[ele]]["unit_type"]
            self.ingredients.pop(replaced[ele])
            self.ingredients[replacement[ele]] = dic

        for i in range(len(self.steps)):
            new_lis_ing = []
            new_lis_app = []
            new_lis_tools = []
            for ing in self.steps[i]["ingredients"]:
                if ing in replaced:
                    new_lis_ing.append(replacement[replaced.index(ing)])
                    self.steps[i]["raw"] = self.steps[i]["raw"].replace(ing, replacement[replaced.index(ing)])
                else:
                    new_lis_ing.append(ing)
            self.steps[i]["ingredients"] = new_lis_ing

            for app in self.steps[i]["methods"]:
                if app in data.Chinese["approach"]:
                    new_lis_app.append(data.Chinese["approach"][app])
                    self.steps[i]["raw"] = self.steps[i]["raw"].replace(app, data.Chinese["approach"][app])
                else:
                    new_lis_app.append(app)
            self.steps[i]["methods"] = new_lis_app

            for app in self.steps[i]["tools"]:
                if app in data.Chinese["tools"]:
                    new_lis_tools.append(data.Chinese["tools"][app])
                    self.steps[i]["raw"] = self.steps[i]["raw"].replace(app, data.Chinese["tools"][app])
                else:
                    new_lis_tools.append(app)
            self.steps[i]["tools"] = new_lis_tools
        self.process_methods(self.steps)
        return True


    def indian(self):
        replaced = []
        replacement = []
        det = False
        present = defaultdict(list)
        for ele in self.ingredients.keys():
            if ele in data.Indian["ingredients"]:
                replaced.append(ele)
                replacement.append(data.Indian["ingredients"][ele])
                present["Ingredient Change: "].append([replaced[-1], replacement[-1]])
                det = True
        for i in range(len(self.steps)):
            for app in self.steps[i]["methods"]:
                if app in data.Indian["approach"]:
                    present["Method Change: "].append([app, data.Indian["approach"][app]])
                    det = True
            for app in self.steps[i]["tools"]:
                if app in data.Indian["tools"]:
                    present["Tool Change: "].append([app, data.Indian["tools"][app]])
                    det = True
        if not det:
            print("Sorry, we cannot find any transformations. This particular recipe could not be made in Indian style.")
            return False
        else:
            print("We found the following substitutions: ")
            for keys in present:
                print(keys, present[keys])

        for ele in range(len(replaced)):
            dic = {}
            dic["name"] = replacement[ele]
            dic["quantity"] = self.ingredients[replaced[ele]]["quantity"]
            dic["unit"] = self.ingredients[replaced[ele]]["unit"]
            dic["prep"] = self.ingredients[replaced[ele]]["prep"]
            dic["descriptions"] = self.ingredients[replaced[ele]]["descriptions"]
            dic["additional"] = self.ingredients[replaced[ele]]["additional"]
            dic["unit_type"] = self.ingredients[replaced[ele]]["unit_type"]
            self.ingredients.pop(replaced[ele])
            self.ingredients[replacement[ele]] = dic

        for i in range(len(self.steps)):
            new_lis_ing = []
            new_lis_app = []
            new_lis_tools = []
            for ing in self.steps[i]["ingredients"]:
                if ing in replaced:
                    new_lis_ing.append(replacement[replaced.index(ing)])
                    self.steps[i]["raw"] = self.steps[i]["raw"].replace(ing, replacement[replaced.index(ing)])
                else:
                    new_lis_ing.append(ing)
            self.steps[i]["ingredients"] = new_lis_ing

            for app in self.steps[i]["methods"]:
                if app in data.Indian["approach"]:
                    new_lis_app.append(data.Indian["approach"][app])
                    self.steps[i]["raw"] = self.steps[i]["raw"].replace(app, data.Indian["approach"][app])
                else:
                    new_lis_app.append(app)
            self.steps[i]["methods"] = new_lis_app

            for app in self.steps[i]["tools"]:
                if app in data.Indian["tools"]:
                    new_lis_tools.append(data.Indian["tools"][app])
                    self.steps[i]["raw"] = self.steps[i]["raw"].replace(app, data.Indian["tools"][app])
                else:
                    new_lis_tools.append(app)
            self.steps[i]["tools"] = new_lis_tools
        self.process_methods(self.steps)
        return True


    def french(self):
        replaced = []
        replacement = []
        det = False
        present = defaultdict(list)
        for ele in self.ingredients.keys():
            if ele in data.French["ingredients"]:
                replaced.append(ele)
                replacement.append(data.French["ingredients"][ele])
                present["Ingredient Change: "].append([replaced[-1], replacement[-1]])
                det = True
        for i in range(len(self.steps)):
            for app in self.steps[i]["methods"]:
                if app in data.French["approach"]:
                    present["Method Change: "].append([app, data.French["approach"][app]])
                    det = True
            for app in self.steps[i]["tools"]:
                if app in data.French["tools"]:
                    present["Tool Change: "].append([app, data.French["tools"][app]])
                    det = True
        if not det:
            print("Sorry, we cannot find any transformations. This particular recipe could not be made in French style.")
            return False
        else:
            print("We found the following substitutions: ")
            for keys in present:
                print(keys, present[keys])

        for ele in range(len(replaced)):
            dic = {}
            dic["name"] = replacement[ele]
            dic["quantity"] = self.ingredients[replaced[ele]]["quantity"]
            dic["unit"] = self.ingredients[replaced[ele]]["unit"]
            dic["prep"] = self.ingredients[replaced[ele]]["prep"]
            dic["descriptions"] = self.ingredients[replaced[ele]]["descriptions"]
            dic["additional"] = self.ingredients[replaced[ele]]["additional"]
            dic["unit_type"] = self.ingredients[replaced[ele]]["unit_type"]
            self.ingredients.pop(replaced[ele])
            self.ingredients[replacement[ele]] = dic

        for i in range(len(self.steps)):
            new_lis_ing = []
            new_lis_app = []
            new_lis_tools = []
            for ing in self.steps[i]["ingredients"]:
                if ing in replaced:
                    new_lis_ing.append(replacement[replaced.index(ing)])
                    self.steps[i]["raw"] = self.steps[i]["raw"].replace(ing, replacement[replaced.index(ing)])
                else:
                    new_lis_ing.append(ing)
            self.steps[i]["ingredients"] = new_lis_ing

            for app in self.steps[i]["methods"]:
                if app in data.French["approach"]:
                    new_lis_app.append(data.French["approach"][app])
                    self.steps[i]["raw"] = self.steps[i]["raw"].replace(app, data.French["approach"][app])
                else:
                    new_lis_app.append(app)
            self.steps[i]["methods"] = new_lis_app

            for app in self.steps[i]["tools"]:
                if app in data.French["tools"]:
                    new_lis_tools.append(data.French["tools"][app])
                    self.steps[i]["raw"] = self.steps[i]["raw"].replace(app, data.French["tools"][app])
                else:
                    new_lis_tools.append(app)
            self.steps[i]["tools"] = new_lis_tools
        self.process_methods(self.steps)
        return True


    def mexico(self):
        replaced = []
        replacement = []
        det = False
        present = defaultdict(list)
        for ele in self.ingredients.keys():
            if ele in data.Mexican["ingredients"]:
                replaced.append(ele)
                replacement.append(data.Mexican["ingredients"][ele])
                present["Ingredient Change: "].append([replaced[-1], replacement[-1]])
                det = True
        for i in range(len(self.steps)):
            for app in self.steps[i]["methods"]:
                if app in data.Mexican["approach"]:
                    present["Method Change: "].append([app, data.Mexican["approach"][app]])
                    det = True
            for app in self.steps[i]["tools"]:
                if app in data.Mexican["tools"]:
                    present["Tool Change: "].append([app, data.Mexican["tools"][app]])
                    det = True
        if not det:
            print("Sorry, we cannot find any transformations. This particular recipe could not be made in Mexican style.")
            return False
        else:
            print("We found the following substitutions: ")
            for keys in present:
                print(keys, present[keys])

        for ele in range(len(replaced)):
            dic = {}
            dic["name"] = replacement[ele]
            dic["quantity"] = self.ingredients[replaced[ele]]["quantity"]
            dic["unit"] = self.ingredients[replaced[ele]]["unit"]
            dic["prep"] = self.ingredients[replaced[ele]]["prep"]
            dic["descriptions"] = self.ingredients[replaced[ele]]["descriptions"]
            dic["additional"] = self.ingredients[replaced[ele]]["additional"]
            dic["unit_type"] = self.ingredients[replaced[ele]]["unit_type"]
            self.ingredients.pop(replaced[ele])
            self.ingredients[replacement[ele]] = dic

        for i in range(len(self.steps)):
            new_lis_ing = []
            new_lis_app = []
            new_lis_tools = []
            for ing in self.steps[i]["ingredients"]:
                if ing in replaced:
                    new_lis_ing.append(replacement[replaced.index(ing)])
                    self.steps[i]["raw"] = self.steps[i]["raw"].replace(ing, replacement[replaced.index(ing)])
                else:
                    new_lis_ing.append(ing)
            self.steps[i]["ingredients"] = new_lis_ing

            for app in self.steps[i]["methods"]:
                if app in data.Mexican["approach"]:
                    new_lis_app.append(data.Mexican["approach"][app])
                    self.steps[i]["raw"] = self.steps[i]["raw"].replace(app, data.Mexican["approach"][app])
                else:
                    new_lis_app.append(app)
            self.steps[i]["methods"] = new_lis_app

            for app in self.steps[i]["tools"]:
                if app in data.Mexican["tools"]:
                    new_lis_tools.append(data.Mexican["tools"][app])
                    self.steps[i]["raw"] = self.steps[i]["raw"].replace(app, data.Mexican["tools"][app])
                else:
                    new_lis_tools.append(app)
            self.steps[i]["tools"] = new_lis_tools
        self.process_methods(self.steps)
        return True

    def cajun(self):
        replaced = []
        replacement = []
        det = False
        present = defaultdict(list)
        for ele in self.ingredients.keys():
            if ele in data.Cajun["ingredients"]:
                replaced.append(ele)
                replacement.append(data.Cajun["ingredients"][ele])
                present["Ingredient Change: "].append([replaced[-1], replacement[-1]])
                det = True
        for i in range(len(self.steps)):
            for app in self.steps[i]["methods"]:
                if app in data.Cajun["approach"]:
                    present["Method Change: "].append([app, data.Cajun["approach"][app]])
                    det = True
            for app in self.steps[i]["tools"]:
                if app in data.Cajun["tools"]:
                    present["Tool Change: "].append([app, data.Cajun["tools"][app]])
                    det = True
        if not det:
            print("Sorry, we cannot find any transformations. This particular recipe could not be made in Cajun style.")
            return False
        else:
            print("We found the following substitutions: ")
            for keys in present:
                print(keys, present[keys])

        for ele in range(len(replaced)):
            dic = {}
            dic["name"] = replacement[ele]
            dic["quantity"] = self.ingredients[replaced[ele]]["quantity"]
            dic["unit"] = self.ingredients[replaced[ele]]["unit"]
            dic["prep"] = self.ingredients[replaced[ele]]["prep"]
            dic["descriptions"] = self.ingredients[replaced[ele]]["descriptions"]
            dic["additional"] = self.ingredients[replaced[ele]]["additional"]
            dic["unit_type"] = self.ingredients[replaced[ele]]["unit_type"]
            self.ingredients.pop(replaced[ele])
            self.ingredients[replacement[ele]] = dic

        for i in range(len(self.steps)):
            new_lis_ing = []
            new_lis_app = []
            new_lis_tools = []
            for ing in self.steps[i]["ingredients"]:
                if ing in replaced:
                    new_lis_ing.append(replacement[replaced.index(ing)])
                    self.steps[i]["raw"] = self.steps[i]["raw"].replace(ing, replacement[replaced.index(ing)])
                else:
                    new_lis_ing.append(ing)
            self.steps[i]["ingredients"] = new_lis_ing

            for app in self.steps[i]["methods"]:
                if app in data.Cajun["approach"]:
                    new_lis_app.append(data.Cajun["approach"][app])
                    self.steps[i]["raw"] = self.steps[i]["raw"].replace(app, data.Cajun["approach"][app])
                else:
                    new_lis_app.append(app)
            self.steps[i]["methods"] = new_lis_app

            for app in self.steps[i]["tools"]:
                if app in data.Cajun["tools"]:
                    new_lis_tools.append(data.Cajun["tools"][app])
                    self.steps[i]["raw"] = self.steps[i]["raw"].replace(app, data.Cajun["tools"][app])
                else:
                    new_lis_tools.append(app)
            self.steps[i]["tools"] = new_lis_tools
        self.process_methods(self.steps)
        return True

    def lactose_free(self):
        replaced = []
        replacement = []
        det = False
        present = defaultdict(list)
        des_rep=set()

        for ele in self.ingredients.keys():

            if ele in data.Lactose_Free:
                replaced.append(ele)
                replacement.append(data.Lactose_Free[ele])
                present["Ingredient Change: "].append([replaced[-1], replacement[-1]])
                det = True
            elif "cheese" in ele:
                replaced.append(ele)
                replacement.append("plant-based "+ele)
                present["Ingredient Change: "].append([replaced[-1], replacement[-1]])
                det = True

        if not det:
            print("Sorry, we cannot find any transformation. This recipe is already lactose free")
            return False
        else:
            print("We found the following substitutions: ")
            for keys in present:
                print(keys, present[keys])

        for ele in range(len(replaced)):
            dic = {}
            dic["name"] = replacement[ele]
            dic["quantity"] = self.ingredients[replaced[ele]]["quantity"]
            dic["unit"] = self.ingredients[replaced[ele]]["unit"]
            dic["prep"] = self.ingredients[replaced[ele]]["prep"]
            dic["descriptions"] = []
            dic["unit_type"] = self.ingredients[replaced[ele]]["unit_type"]
            for w in self.ingredients[replaced[ele]]["descriptions"]:
                if w not in data.descriptors["dairy"]:
                    dic["descriptions"].append(w)
                else:
                    des_rep.add(w)
            dic["additional"] = self.ingredients[replaced[ele]]["additional"]
            if replacement[ele] in self.ingredients:
                self.ingredients.pop(replaced[ele])
                if self.ingredients[replacement[ele]]["unit"] == dic["unit"]:
                    self.ingredients[replacement[ele]]["quantity"] += dic["quantity"]
                else:
                    u = []
                    q = []
                    u.append(self.ingredients[replacement[ele]]["unit"])
                    u.append(dic["unit"])
                    q.append(self.ingredients[replacement[ele]]["quantity"])
                    q.append(dic["quantity"])
                    self.ingredients[replacement[ele]]["quantity"] = q
                    self.ingredients[replacement[ele]]["unit"] = u
                    self.ingredients[replacement[ele]]["descriptions"] += dic["descriptions"]
                    self.ingredients[replacement[ele]]["prep"] += dic["prep"]

            else:
                self.ingredients.pop(replaced[ele])
                self.ingredients[replacement[ele]] = dic

        for i in range(len(self.steps)):
            new_lis_ing = []
            for ing in self.steps[i]["ingredients"]:
                if ing in replaced:
                    new_lis_ing.append(replacement[replaced.index(ing)])
                    self.steps[i]["raw"] = self.steps[i]["raw"].replace(ing, replacement[replaced.index(ing)])

                else:
                    new_lis_ing.append(ing)
            spl=self.steps[i]["raw"].split()
            for words in spl:
                if words in des_rep:
                    self.steps[i]["raw"] = self.steps[i]["raw"].replace(words,"")
                    self.steps[i]["raw"] = self.steps[i]["raw"].replace("  ", " ")
            self.steps[i]["ingredients"] = new_lis_ing
        return True

    def to_stir_fry(self):
        det=False
        approach=[]
        for s in self.steps:
            for w in s["raw"].split():
                if w in data.Cook_Approach and w!='stir-fry':
                    det=True
                    if w not in approach:
                        approach.append(w)
        if not det:
            print("Sorry, we cannot find any cooking methods that can be transformed to stir-fry.")
            return False
        else:
            print("We will transform the following method to stir-fry: ",approach)

        if "vegetable oil" not in self.ingredients:
            dic = {}
            dic["name"] = "vegetable oil"
            dic["quantity"] = 2.0
            dic["unit"] = "teaspoon"
            dic["prep"] = []
            dic["descriptions"] = []
            dic["additional"] = ["Add before stir fry"]
            dic['unit_type']="volumetric"
            self.ingredients["vegetable oil"]=dic

        for index in range(len(self.steps)):
            for w in self.steps[index]["raw"].split():
                if w in data.Cook_Approach:
                    self.steps[index]["raw"]=self.steps[index]["raw"].replace(w,"stir fry")
                if w in data.Approach_Tools:
                    self.steps[index]["raw"] = self.steps[index]["raw"].replace(w, "wok")
            new_t=[]
            for t in self.steps[index]["tools"]:
                if t in data.Approach_Tools:
                    if "wok" not in new_t:
                        new_t.append("wok")
                else:
                    new_t.append(t)
            self.steps[index]["tools"]=new_t

            new_met = []
            for m in self.steps[index]["methods"]:
                if m in data.Cook_Approach:
                    if "stir-fry" not in new_met:
                        new_met.append("stir-fry")
                else:
                    new_met.append(m)
            self.steps[index]["methods"] = new_met

        return True

    def to_steam(self):
        det=False
        approach=[]
        for s in self.steps:
            for w in s["raw"].split():
                if w in data.Cook_Approach and w!='steam':
                    det=True
                    if w not in approach:
                        approach.append(w)
        if not det:
            print("Sorry, we cannot find any cooking methods that can be transformed to steaming.")
            return False
        else:
            print("We will transform the following method to steaming: ",approach)

        if "water" not in self.ingredients:
            dic = {}
            dic["name"] = "water"
            dic["quantity"] = 1
            dic["unit"] = "Based on the size of steamer"
            dic["prep"] = []
            dic["descriptions"] = []
            dic["additional"] = ["Add before steam"]
            dic["unit_type"]="N/A"
            self.ingredients["water"]=dic
        else:
            dic = {}
            dic["name"] = "water for steaming"
            dic["quantity"] = 1
            dic["unit"] = "Based on the size of steamer"
            dic["prep"] = []
            dic["descriptions"] = []
            dic["additional"] = ["Add before steam"]
            dic["unit_type"] = "N/A"
            self.ingredients["water for steaming"] = dic


        for index in range(len(self.steps)):
            for w in self.steps[index]["raw"].split():
                if w in data.Cook_Approach:
                    self.steps[index]["raw"]=self.steps[index]["raw"].replace(w,"steam")
                if w in data.Approach_Tools:
                    self.steps[index]["raw"] = self.steps[index]["raw"].replace(w, "steamer")
            new_t=[]
            for t in self.steps[index]["tools"]:
                if t in data.Approach_Tools:
                    if "steamer" not in new_t:
                        new_t.append("steamer")
                else:
                    new_t.append(t)
            self.steps[index]["tools"]=new_t

            new_met=[]
            for m in self.steps[index]["methods"]:
                if m in data.Cook_Approach:
                    if "steam" not in new_met:
                        new_met.append("steam")
                else:
                    new_met.append(m)
            self.steps[index]["methods"]=new_met

        new_step={
            "raw":"add water to steamer",
            "time":{},
            "tools":[],
            "methods":["add"],
            "ingredients":['water']
        }
        self.steps=[new_step]+self.steps
        return True

    def to_deep_fry(self):
        det=False
        approach=[]
        for s in self.steps:
            for w in s["raw"].split():
                if w in data.Cook_Approach and w!='deep-fry':
                    det=True
                    if w not in approach:
                        approach.append(w)
        if not det:
            print("Sorry, we cannot find any cooking methods that can be transformed to deep-fry.")
            return False
        else:
            print("We will transform the following method to deep-fry: ",approach)

        if "vegetable oil" not in self.ingredients:
            dic = {}
            dic["name"] = "vegetable oil"
            dic["quantity"] = 1
            dic["unit"] = "Based on the size of fryer"
            dic["prep"] = []
            dic["descriptions"] = []
            dic["additional"] = ["Add before deep-fry"]
            dic["unit_type"] = "N/A"
            self.ingredients["vegetable oil"]=dic
        else:
            dic = {}
            dic["name"] = "frying vegetable oil"
            dic["quantity"] = 1
            dic["unit"] = "Based on the size of fryer"
            dic["prep"] = []
            dic["descriptions"] = []
            dic["additional"] = ["Add before deep-fry"]
            dic["unit_type"] = "N/A"
            self.ingredients["frying vegetable oil"] = dic

        if "flour" not in self.ingredients:
            dic = {}
            dic["name"] = "flour"
            dic["quantity"] = 1
            dic["unit"] = "Based on the ingredients"
            dic["prep"] = []
            dic["descriptions"] = []
            dic["additional"] = ["cover ingredients"]
            dic["unit_type"] = "N/A"

            self.ingredients["flour"]=dic
        else:
            self.ingredients["flour"]["quantity"]+=1.0


        for index in range(len(self.steps)):
            for w in self.steps[index]["raw"].split():
                if w in data.Cook_Approach:
                    self.steps[index]["raw"]=self.steps[index]["raw"].replace(w,"deep-fry")
                if w in data.Approach_Tools:
                    self.steps[index]["raw"] = self.steps[index]["raw"].replace(w, "deep-fryer")
            new_t=[]
            for t in self.steps[index]["tools"]:
                if t in data.Approach_Tools:
                    if "deep-fryer" not in new_t:
                        new_t.append("deep-fryer")
                else:
                    new_t.append(t)
            self.steps[index]["tools"]=new_t

            new_met=[]
            for m in self.steps[index]["methods"]:
                if m in data.Cook_Approach:
                    if "deep-fry" not in new_met:
                        new_met.append("deep-fry")
                else:
                    new_met.append(m)
            self.steps[index]["methods"]=new_met

        new_step={
            "raw":"cover main ingredients with flour",
            "time":{},
            "tools":[],
            "methods":["cover"],
            "ingredients":['flour']
        }
        self.steps=[new_step]+self.steps
        return True

    def to_bake(self):
        det=False
        approach=[]
        for s in self.steps:
            for w in s["raw"].split():
                if w in data.Cook_Approach and w!='bake':
                    det=True
                    if w not in approach:
                        approach.append(w)
        if not det:
            print("Sorry, we cannot find any cooking methods that can be transformed to baking.")
            return False
        else:
            print("We will transform the following method to baking: ",approach)

        preheat=False
        for index in range(len(self.steps)):
            for w in self.steps[index]["raw"].split():
                if w in data.Cook_Approach:
                    self.steps[index]["raw"]=self.steps[index]["raw"].replace(w,"bake")
                if w in data.Approach_Tools:
                    self.steps[index]["raw"] = self.steps[index]["raw"].replace(w, "oven")
                if w=="preheat":
                    preheat=True
            new_t=[]
            for t in self.steps[index]["tools"]:
                if t in data.Approach_Tools:
                    if "oven" not in new_t:
                        new_t.append("oven")
                else:
                    new_t.append(t)
            self.steps[index]["tools"]=new_t

            new_met=[]
            for m in self.steps[index]["methods"]:
                if m in data.Cook_Approach:
                    if "bake" not in new_met:
                        new_met.append("bake")
                else:
                    new_met.append(m)
            self.steps[index]["methods"]=new_met
        if not preheat:
            new_step={
                "raw":"preheat oven to 400°F",
                "time":{},
                "tools":["oven"],
                "methods":["preheat"],
                "ingredients":[]
            }
            self.steps=[new_step]+self.steps
        return True

    def new_ingredient_processor(self, soupy):
        ingredients_list = soupy.find_all(id=re.compile("^recipe-ingredients-label"))
        ingredients_dic = {}

        for i in ingredients_list:
            unit = i.attrs["data-unit"]
            if unit == "":
                unit = "unit"
            unit_type = i.attrs["data-unit_family"]
            if unit_type == "":
                unit_type = "each"
            
            quantity = i.attrs["data-init-quantity"]
            ingredient = i.attrs["data-ingredient"]
            split_ing = re.split("\s|,", ingredient)
            prep = []
            new_ing = []
            description = []
            additional = []
            for j in split_ing:
                if j.strip() in data.prep:
                    prep.append(j.strip())
                elif j.strip() in data.descriptors_non_nation:
                    description.append(j.strip())
                elif j.strip() not in set(["to", "or", "taste", "and", "into", "for", "as", "needed"]):
                    new_ing.append(j.strip())

            for k in range(len(new_ing)):
                new_ing[k]=new_ing[k].strip()
                new_ing[k]=new_ing[k].lower()

            for k in range(len(prep)):
                prep[k]=prep[k].strip()

            for k in range(len(description)):
                description[k]=description[k].strip()



            new_ing_name = " ".join(new_ing)
            words=new_ing
            e=0
            while e < len(words):
                if len(words[e])==0:
                    e+=1
                    continue
                elif words[e][0] == "(":
                    desc = words[e][1:]
                    if ")" in words[e]:
                        desc=desc.replace(")", "")
                        new_ing_name = new_ing_name.replace(words[e], "")
                        new_ing_name = new_ing_name.replace("  ", " ")
                        break
                    else:
                        new_ing_name = new_ing_name.replace(words[e], "")
                        new_ing_name = new_ing_name.replace("  ", " ")
                    e += 1
                    while e < len(words) and words[e][-1] != ")":
                        new_ing_name = new_ing_name.replace(words[e], "")
                        new_ing_name = new_ing_name.replace("  ", " ")
                        desc += " " + words[e]
                        e += 1
                    if e<len(words):
                        new_ing_name = new_ing_name.replace(words[e], "")
                        new_ing_name = new_ing_name.replace("  ", " ")
                        desc +=" "+ words[e][:len(words[e]) - 1]
                    additional.append(desc)
                e += 1
            #Handle parenthesise
            new_ing_name=new_ing_name.replace("-inch"," inch")
            update=new_ing_name.split()
            #print(update)
            for w in range(len(update)):
                temp=update[w].strip()
                if temp in data.Liquid_Measurements or temp in data.Solid_Measurements:
                    if w > 0:
                        try:
                            q = float(update[w - 1])
                            unit = temp
                            new_ing_name = new_ing_name.replace(update[w], "")
                            new_ing_name = new_ing_name.replace(update[w - 1], "")
                            new_ing_name = new_ing_name.replace("  ", "")
                            additional.append(str(q) + " " + unit)
                        except:
                            try:
                                q = float(Fraction(update[w - 1]))
                                add = str(q) + " " + update[w]
                                additional.append(add)
                                new_ing_name = new_ing_name.replace(update[w], "")
                                new_ing_name = new_ing_name.replace(update[w - 1], "")
                                new_ing_name = new_ing_name.replace("  ", "")
                            except:
                                continue
            #handling description with units

            dic={}
            new_ing_name=new_ing_name.replace(" - "," ")
            new_ing_name=new_ing_name.replace(" -","")
            new_ing_name=new_ing_name.strip()

            dic["name"] = new_ing_name
            try:
                dic["quantity"] = float(quantity)
            except:
                dic["quantity"] = 0
            dic["prep"] = prep
            dic["descriptions"] = description
            dic["unit"] = unit
            dic["unit_type"] = unit_type
            dic["additional"] = additional


            if dic["name"] in ingredients_dic and ingredients_dic[new_ing_name]["descriptions"] == dic["descriptions"] and ingredients_dic[dic['name']]["unit"] == dic["unit"] and ingredients_dic[new_ing_name]["prep"] == dic["prep"]:
                ingredients_dic[dic["name"]]["quantity"]+=dic["quantity"]
            elif dic['name'] in ingredients_dic and len(dic["prep"])>0 and ingredients_dic[dic['name']]["prep"]!=dic["prep"]:
                dic['name']=dic['prep'][0]+" "+dic["name"]
                ingredients_dic[dic['name']] = dic
            elif dic['name'] in ingredients_dic and len(ingredients_dic[dic["name"]]["prep"])>0 and ingredients_dic[dic['name']]["prep"]!=dic["prep"]:
                temp=ingredients_dic[dic['name']]
                temp['name']=temp['prep'][0]+" "+temp['name']
                ingredients_dic[temp['name']]=temp
                ingredients_dic[dic['name']] = dic
            elif dic['name'] in ingredients_dic and len(dic["descriptions"])>0 and ingredients_dic[dic['name']]["descriptions"]!=dic["descriptions"]:
                dic['name']=dic['descriptions'][0]+" "+dic["name"]
                ingredients_dic[dic['name']] = dic

            elif dic['name'] in ingredients_dic and len(ingredients_dic[dic["name"]]["descriptions"])>0 and ingredients_dic[dic['name']]["descriptions"]!=dic["descriptions"]:
                temp=ingredients_dic[dic['name']]
                temp['name']=temp['descriptions'][0]+" "+temp['name']
                ingredients_dic[temp['name']]=temp
                ingredients_dic[dic['name']] = dic

            elif dic['name'] in ingredients_dic:
                    dic['name'] = dic["name"]+" for different purpose"
                    ingredients_dic[dic['name']] = dic
            else:
                ingredients_dic[dic['name']]=dic

        return ingredients_dic

    def original_cuisine(self):
        most_likely = {}
        # for j in self.ingredients.keys():
        #     print(j)
        for i in data.Region.keys():
            for j in self.ingredients.keys():
                #print(j)
                if j in data.Region[i]:
                    #print(i, j)
                    if i in most_likely.keys():
                        most_likely[i].append(j)
                    else:
                        most_likely[i] = [j]
        maxim = []
        maximv = 0
        ingr = []
        for i in most_likely.keys():
            if len(most_likely[i]) == maximv:
                maxim.append(i)
                ingr.append(most_likely[i])
            if len(most_likely[i]) > maximv:
                maxim = [i]
                maximv = len(most_likely[i])
                ingr = [most_likely[i]]

        return maxim, ingr

    def initialize(self,url):
        self.ingredients = {}
        self.primary_method = []
        self.secondary_method = []
        self.steps = []
        self.title=""
        self.__init__(url)


    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        setattr(result, 'primary_method', [copy.deepcopy(x) for x in self.primary_method])
        setattr(result, 'secondary_method', [copy.deepcopy(x) for x in self.secondary_method])
        setattr(result, 'steps', [copy.deepcopy(x) for x in self.steps])
        setattr(result, 'ingredients', copy.deepcopy(self.ingredients))
        setattr(result, 'title', copy.deepcopy(self.title))
        return result

    def print_title(self):
        print('\n')
        print("Recipe Name: ",self.title)


    def __init__(self,dish):
        html = requests.get(dish)

        bs=BeautifulSoup(html.content, features="html.parser")
        #print(bs)
        self.title=bs.find('title').string
        self.title=self.title.replace(" | Allrecipes","")
        self.title=self.title.strip()
        self.title=self.title.lower()
        print("\n")
        print("Target Recipe: ",self.title)
        #new simplified ingredient parser
        self.ingredients = self.new_ingredient_processor(bs)


        ### original ingredients processing
        # res=bs.find_all("span",attrs={"class": "ingredients-item-name"})
        # for ele in res:
        #     #print(ele.get_text())
        #     s=ele.get_text().split()
        #     separate=-1
        #     for i in range(len(s)):
        #         if s[i]=="and" and i>0 and s[i-1] not in data.prep:
        #             separate=i
        #     if separate==-1:
        #         #print(ele.get_text())
        #         temp=self.process_ingredients(ele.get_text())
        #         #print (temp)
        #         if temp['name'] in self.ingredients and self.ingredients[temp['name']]["descriptions"]==temp["descriptions"] and self.ingredients[temp['name']]["unit"]==temp["unit"] and self.ingredients[temp['name']]["prep"]==temp["prep"]:
        #             self.ingredients[temp["name"]]["quantity"]+=temp["quantity"]
        #         elif temp['name'] in self.ingredients and len(temp["prep"])>0 and self.ingredients[temp['name']]["prep"]!=temp["prep"]:
        #             temp['name']=temp['prep'][0]+" "+temp["name"]
        #             self.ingredients[temp['name']] = temp
        #         elif temp['name'] in self.ingredients and len(temp["descriptions"])>0 and self.ingredients[temp['name']]["descriptions"]!=temp["descriptions"]:
        #             temp['name']=temp['descriptions'][0]+" "+temp["name"]
        #             self.ingredients[temp['name']] = temp
        #         elif temp['name'] in self.ingredients:
        #             temp['name'] = temp["name"]+" for different purpose"
        #             self.ingredients[temp['name']] = temp
        #         else:
        #             self.ingredients[temp['name']]=temp
        #     else:
        #         temp = self.process_ingredients(" ".join(s[:separate]))
        #         if temp:
        #             self.ingredients[temp['name']] = temp
        #         temp = self.process_ingredients(" ".join(s[separate+1:]))
        #         if temp and len(temp['name'])>3:
        #             self.ingredients[temp['name']] = temp
        # print(self.ingredients)

        print("Ingredients Parsing Finished")
        #Find Ingredients
        #self.original_cuisine()

        res = bs.find_all("li", attrs={"class": "subcontainer instructions-section-item"})

        self.process_methods_bs(res)
        #Find Secondary Method

        for ele in res:
            #print(ingredients.keys())
            self.steps+=self.process_steps(ele.get_text())


