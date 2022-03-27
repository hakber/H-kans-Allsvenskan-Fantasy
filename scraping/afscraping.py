#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 11:21:57 2022

@author: hakanbernhardsson
"""

from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

story="https://fantasy.allsvenskan.se/statistics"
players=[]

antalSidor=14

driver = webdriver.Firefox()


driver.get(story)
allPlayers=[]

for sidor in range((antalSidor)):
    players = driver.find_elements_by_xpath('//button[@title="Se spelarinformation"]')
    
    for player in players:
        player.click()
        
        namn= driver.find_elements_by_xpath("/html/body/div[2]/div/dialog/div/div[1]/div[1]/div/div")[0].text
        print(namn)
        
        pris= driver.find_elements_by_xpath("/html/body/div[2]/div/dialog/div/div[1]/div[1]/div/span")[0].text
        print(pris)
        
        position=""
        divnummer=1
        positionFind=driver.find_elements_by_xpath("/html/body/div[2]/div/dialog/div/div[2]/div[1]/div/div[1]/div[3]/ul/li[1]/div")
        if len(positionFind)>0:
            position=positionFind[0].text
        else:
            divnummer=2
            positionFind=driver.find_elements_by_xpath("/html/body/div[2]/div/dialog/div/div[2]/div[2]/div/div[1]/div[3]/ul/li[1]/div")
            position=positionFind[0].text
        print(position)

        klubbtext=""
        klubb=driver.find_elements_by_xpath("/html/body/div[2]/div/dialog/div/div[2]/div["+str(divnummer)+"]/div/div[1]/div[2]/img")
        if len(klubb)>0:
            klubbtext=klubb[0].get_attribute("alt")[24:]
            print(klubbtext)
        
        #Gå till historia
        
        driver.find_elements_by_xpath("/html/body/div[2]/div/dialog/div/div[2]/ul/li[2]/a")[0].click()
        
        #/html/body/div[2]/div/dialog/div/div[2]/div[2]/div[4]/div/table/thead/tr/th[1]
        #SÄTT IN EN TVÅA HÄR
        
        rows=1+len(driver.find_elements_by_xpath("/html/body/div[2]/div/dialog/div/div[2]/div["+str(divnummer)+"]/div[4]/div/table/tbody/tr"))
        #tabell=driver.find_elements_by_xpath("/html/body/div[2]/div/dialog/div/div[2]/div[1]/div[4]/div/table")
        print(rows)
        
        columns=len(driver.find_elements_by_xpath("/html/body/div[2]/div/dialog/div/div[2]/div["+str(divnummer)+"]/div[4]/div/table/tbody/tr/td"))
        print(columns)
        

        #print(players)
        #sleep(3)
        
        seasons=[]
        for r in range(1, rows):
            seasonStats=[]
            for p in range(1, 23):
                value = driver.find_element_by_xpath("/html/body/div[2]/div/dialog/div/div[2]/div["+str(divnummer)+"]/div[4]/div/table/tbody/tr["+str(r)+"]/td["+str(p)+"]").text
                seasonStats.append(value)
            rubriker=["Säsong","Totalpoäng","Gjorda mål","Assists","Hållna nollor","Insläppta mål","Räddade straffar","Missade straffar","Gula kort","Röda kort","Räddningar","Självmål","Offensiva bonuspoäng","Defensiva bonuspoäng","Avgörande mål","Inlägg","Nyckelpassningar","Skapade klara chanser","Clearances, blocks, interceptions and recoveries","Bollåtererövringar","Kronor start av säsong","Kronor slut av säsong"]
            seasonStatsLabel=zip(rubriker,seasonStats)
            seasons.append(dict(seasonStatsLabel))
        #sleep(3)
        print(seasons)
        
        rubriker2=["Namn","Klubb","Position","Pris","Säsongsdata"]
        playerStatsLabel=zip(rubriker2, [namn,klubbtext,position,pris,seasons] )
        allPlayers.append(dict(playerStatsLabel))
        
        driver.find_elements_by_xpath("/html/body/div[2]/div/dialog/div/div[2]/ul/li[2]/a")[0].send_keys(Keys.ESCAPE);
    
    driver.find_elements_by_xpath("/html/body/div[1]/div/div[2]/div/div/div[4]/button[3]")[0].click()

# k, cool. let's bounce. 
driver.quit()

import pandas as pd
players_df=pd.DataFrame(allPlayers)
#pd.json_normalize(allPlayers["Value"])
players_df["Pris"]=players_df["Pris"].str.slice(stop=-3)
players_df["Pris"]=pd.to_numeric(players_df["Pris"])

players_df.to_json("players.json")

spelarmappning=pd.read_excel("../data/spelarmappning.xlsx")
outDf=players_df.merge(spelarmappning, on=["Namn","Klubb"])

##Gör någonting ovan åt omatchade rader