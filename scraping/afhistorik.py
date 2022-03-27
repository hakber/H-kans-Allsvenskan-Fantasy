#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 13:46:16 2022

@author: hakanbernhardsson
"""

import pandas as pd

kolumner=["Säsong","Totalpoäng","Gjorda mål","Assists","Hållna nollor","Insläppta mål","Räddade straffar","Missade straffar","Gula kort","Röda kort","Räddningar","Självmål","Offensiva bonuspoäng","Defensiva bonuspoäng","Avgörande mål","Inlägg","Nyckelpassningar","Skapade klara chanser","Clearances, blocks, interceptions and recoveries","Bollåtererövringar","Kronor start av säsong","Kronor slut av säsong", 'id']

player_frame=pd.read_json("players.json")
spelarmappning=pd.read_excel("../data/spelarmappning.xlsx")

player_frame['id'] = player_frame.index
player_frame=player_frame.merge(spelarmappning, on=["id"], how="left")

firstNormalize=pd.json_normalize(player_frame["Säsongsdata"])

allHistory=pd.DataFrame()

for column in firstNormalize.columns:
    tempNormalize=pd.json_normalize(firstNormalize[column])
    tempNormalize["id"]=player_frame["id"]
    tempNormalize.columns=kolumner
    allHistory=allHistory.append(tempNormalize)
    
allHistory=allHistory[allHistory["Säsong"].notnull()]

#Byt ordning
allHistory=allHistory[['id', "Säsong","Totalpoäng","Gjorda mål","Assists","Hållna nollor","Insläppta mål","Räddade straffar","Missade straffar","Gula kort","Röda kort","Räddningar","Självmål","Offensiva bonuspoäng","Defensiva bonuspoäng","Avgörande mål","Inlägg","Nyckelpassningar","Skapade klara chanser","Clearances, blocks, interceptions and recoveries","Bollåtererövringar","Kronor start av säsong","Kronor slut av säsong"]]

allHistory.to_csv("afhistorik.csv", index=False)
