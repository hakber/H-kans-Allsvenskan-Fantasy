#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 15:44:35 2022

@author: hakanbernhardsson
"""

import pandas as pd

def sortPris(val):
    return val["Pris"] 

Cash=100
Num_Gk=2
Num_Def=5
Num_Mid=5
Num_Att=3


spelarlista=pd.read_excel("dataset.xlsx")
spelarlista=spelarlista[['Namn', 'Klubb', 'id', 'Position', 'Pris', 'hb_pred_totpoäng']]
spelarlista["ppkr"]=spelarlista["hb_pred_totpoäng"]/spelarlista["Pris"]

spelarlista=spelarlista.sort_values(by="ppkr", ascending=False)

spelarlista.columns=['Namn', 'Klubb', 'id', 'Position', 'Pris', 'PredP', 'ppkr']
spelarlista=spelarlista.reset_index()

allaSpelare=spelarlista.to_dict("index")

allaKlubbar=spelarlista["Klubb"].unique()
klubbDict={}
for klubb in allaKlubbar:
    klubbDict[klubb]=0
trupp={"value":0, "exp_points":0, "gk":[], "def":[], "mid":[], "att":[], "klubbar":klubbDict  }

#Klubbar-dicten kommer jag inte använda i slutändan, men jag har med den i alla fall om någon annan vill utveckla scriptet

#
#Värdaste elvan
#

for i in allaSpelare:
    if allaSpelare[i]["Position"]=="Målvakt":
        if len(trupp["gk"])<Num_Gk:
            trupp["gk"].append(allaSpelare[i])
            trupp["value"]+=allaSpelare[i]["Pris"]
            trupp["exp_points"]+=allaSpelare[i]["PredP"]
            trupp["klubbar"][allaSpelare[i]["Klubb"]]+=1
    elif allaSpelare[i]["Position"]=="Försvarare":
        if len(trupp["def"])<Num_Def:
            trupp["def"].append(allaSpelare[i])
            trupp["value"]+=allaSpelare[i]["Pris"]
            trupp["exp_points"]+=allaSpelare[i]["PredP"]
            trupp["klubbar"][allaSpelare[i]["Klubb"]]+=1
    elif allaSpelare[i]["Position"]=="Mittfältare":
        if len(trupp["mid"])<Num_Mid:
            trupp["mid"].append(allaSpelare[i])
            trupp["value"]+=allaSpelare[i]["Pris"]
            trupp["exp_points"]+=allaSpelare[i]["PredP"]
            trupp["klubbar"][allaSpelare[i]["Klubb"]]+=1
    elif allaSpelare[i]["Position"]=="Anfallare":
        if len(trupp["att"])<Num_Att:
            trupp["att"].append(allaSpelare[i])
            trupp["value"]+=allaSpelare[i]["Pris"]
            trupp["exp_points"]+=allaSpelare[i]["PredP"]
            trupp["klubbar"][allaSpelare[i]["Klubb"]]+=1

#
# Värdaste elvan skapad
#

trupp["gk"].sort(key=sortPris,reverse=True)
trupp["def"].sort(key=sortPris,reverse=True)
trupp["mid"].sort(key=sortPris,reverse=True)
trupp["att"].sort(key=sortPris,reverse=True)
                
while trupp["value"]<Cash:
    hogstKvot=-1.0
    changepos=""
    changeposWhich=6        
    insertPlayer={}    
        
    for i in allaSpelare:
        if allaSpelare[i]["Position"]=="Målvakt":
            if allaSpelare[i] in trupp["gk"]:
                continue
            else:
                for j in range(Num_Gk):
                    if trupp["value"]-trupp["gk"][j]["Pris"]+allaSpelare[i]["Pris"]<=Cash:
                        if allaSpelare[i]["PredP"]>trupp["gk"][j]["PredP"]:
                            tempKvot=(allaSpelare[i]["PredP"]-trupp["gk"][j]["PredP"])/(allaSpelare[i]["Pris"]-trupp["gk"][j]["Pris"])
                            if tempKvot>hogstKvot:
                                hogstKvot=tempKvot
                                changepos="gk"
                                changeposWhich=j
                                insertPlayer=allaSpelare[i]
        elif allaSpelare[i]["Position"]=="Försvarare":
            if allaSpelare[i] in trupp["def"]:
                continue
            else:
                for j in range(Num_Def):
                    if trupp["value"]-trupp["def"][j]["Pris"]+allaSpelare[i]["Pris"]<=Cash:
                        if allaSpelare[i]["PredP"]>trupp["def"][j]["PredP"]:
                            tempKvot=(allaSpelare[i]["PredP"]-trupp["def"][j]["PredP"])/(allaSpelare[i]["Pris"]-trupp["def"][j]["Pris"])
                            if tempKvot>hogstKvot:
                                hogstKvot=tempKvot
                                changepos="def"
                                changeposWhich=j
                                insertPlayer=allaSpelare[i]
        elif allaSpelare[i]["Position"]=="Mittfältare":
            if allaSpelare[i] in trupp["mid"]:
                continue
            else:
                for j in range(Num_Mid):
                    if trupp["value"]-trupp["mid"][j]["Pris"]+allaSpelare[i]["Pris"]<=Cash:
                        if allaSpelare[i]["PredP"]>trupp["mid"][j]["PredP"]:
                            tempKvot=(allaSpelare[i]["PredP"]-trupp["mid"][j]["PredP"])/(allaSpelare[i]["Pris"]-trupp["mid"][j]["Pris"])
                            if tempKvot>hogstKvot:
                                hogstKvot=tempKvot
                                changepos="mid"
                                changeposWhich=j
                                insertPlayer=allaSpelare[i]
        elif allaSpelare[i]["Position"]=="Anfallare":
            if allaSpelare[i] in trupp["att"]:
                continue
            else:
                for j in range(Num_Att):
                    if trupp["value"]-trupp["att"][j]["Pris"]+allaSpelare[i]["Pris"]<=Cash:
                        if allaSpelare[i]["PredP"]>trupp["att"][j]["PredP"]:
                            tempKvot=(allaSpelare[i]["PredP"]-trupp["att"][j]["PredP"])/(allaSpelare[i]["Pris"]-trupp["att"][j]["Pris"])
                            if tempKvot>hogstKvot:
                                hogstKvot=tempKvot
                                changepos="att"
                                changeposWhich=j
                                insertPlayer=allaSpelare[i]
    print(insertPlayer)
    if changepos!="":
        trupp["exp_points"]=trupp["exp_points"]-trupp[changepos][changeposWhich]["PredP"]+insertPlayer["PredP"]
        trupp["value"]=trupp["value"]-trupp[changepos][changeposWhich]["Pris"]+insertPlayer["Pris"]
        trupp[changepos][changeposWhich]=insertPlayer
        
print(trupp)
    