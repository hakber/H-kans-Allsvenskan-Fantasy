#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 20:20:06 2022

@author: hakanbernhardsson
"""

import requests
from bs4 import BeautifulSoup
import re

import pandas as pd
import json

allMarketValues=pd.DataFrame()

def isNaN(string):
    return string != string

class LazyDecoder(json.JSONDecoder):
    def decode(self, s, **kwargs):
        regex_replacements = [
            (re.compile(r'([^\\])\\([^\\])'), r'\1\\\\\2'),
            (re.compile(r',(\s*])'), r'\1'),
        ]
        for regex, replacement in regex_replacements:
            s = regex.sub(replacement, s)
        return super().decode(s, **kwargs)

headers = {'User-Agent': 
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}


player_df=pd.read_excel("../data/spelarmappning.xlsx")

for index, row in player_df.iterrows():
    if(row["TM_URL"]!="" and isNaN(row["TM_URL"])==False):
        print(row["Namn"])
        print(row["TM_URL"])
        tmNamnTemp=re.search('.com/(.*)/profil/', row["TM_URL"])
        if tmNamnTemp:
            tmNamn=tmNamnTemp.group(1)
            tmNummer= row["TM_URL"][ row["TM_URL"].rfind('/')+1:]
              
            page = "https://www.transfermarkt.com/"+tmNamn+"/marktwertverlauf/spieler/"+tmNummer
            pageTree = requests.get(page, headers=headers)
            pageSoup = BeautifulSoup(pageTree.content, 'html.parser')
            
            elements = pageSoup.findAll('script')
            
            whichNumHasTheJson=0
            for i in range(len(elements)-1,0,-1):
                if("/*<![CDATA[*/" in str(elements[i])):
                    whichNumHasTheJson=i
                    print(i)
                    break
            
            haystack=str(elements[ whichNumHasTheJson ]  )
            needle=re.search('\'series\':(.*),\'credits\'', haystack)
            if needle:
                needleString=str(needle.group(1))
                needleString2 = needleString.replace("\'", "\"")
                
                hej=json.loads(needleString2, cls=LazyDecoder)
                dataDict=hej[0]["data"]
                
                listDf=pd.DataFrame(dataDict)
                listDf["TM_URL"]=row["TM_URL"]
                
                allMarketValues=allMarketValues.append(listDf)

allMarketValues['datum_mw']=allMarketValues['datum_mw'].str.replace('\\', '')
allMarketValues['datum_mw']=allMarketValues['datum_mw'].str.replace('x20', ' ')
allMarketValues['datum_mw']=pd.to_datetime(allMarketValues['datum_mw'])

allMarketValues.to_csv("tmhistorik.csv", index=False)
