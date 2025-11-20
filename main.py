import requests as req
from bs4 import BeautifulSoup as bs
import sqlite3
import time
import getSkullList
from dbcmSqlite import Database
import dbSetup
import re
import json

# Set database if not done yet
dbSetup.dbSetup('skul.db')

# API endpoint
url = "https://skul.fandom.com/api.php"
params = {
        "action": "parse",
        "page": "Skulls",
        "prop": "text",
        "format": "json"
    }
headers = {"User-Agent": "SkulCrawler/1.0"}

def getSoup(url,params,headers):
    print("url= ",url," params= ",str(params)," headers= ",str(headers))
    soup=bs(((req.get(url,params=params,headers=headers)).json())["parse"]["text"]["*"],'lxml')
    time.sleep(1)
    return soup

def getSkulls():
    params["page"]="Skulls"
    soup = getSoup(url,params,headers) 

    exclude = {"Balrog", "Harpy", "Guard Captain", "Slime"}
    skulls=list()
    for td in soup.find_all("td"):
        for li in td.find_all("li"):
            if li.a and "title" in li.a.attrs:
                skullName = li.a["title"]
                if skullName not in exclude:
                    skulls.append(skullName)
    return skulls

# Function to fetch and parse skull page
def getSkullData(skullName):
    skullData={"name":skullName,"description":"","skullType":"","damageType":"","skullInfo":"","basicAttackInfo":"","passiveSkill":"","swapSkillName":"","swapSkillInfo":"","activeSkill":[]}
    params["page"]= skullName.replace(" ","_")
    soup = getSoup(url,params,headers) 
    
    # Get Description
    try:
        skullData["description"]=soup.h3.find_next("i").get_text(strip=True)
    except AttributeError:
        skullData["description"]="MISSING"
        print(f"The description for ? is missing",skullName)

    # Get Skull Type
    try:
        skullData["skullType"]=soup.find("div", {"data-source":"skull_type"}).find_next("div").get_text(strip=True)
    except AttributeError:
        skullData["description"]="MISSING"
        print(f"The description for ? is missing",skullName)

    # Get Damage Type
    try:
        skullData["damageType"]=soup.find("div", {"data-source":"damage_type"}).find_next("div").get_text(strip=True)
    except AttributeError:
        skullData["description"]="MISSING"
        print(f"The description for ? is missing",skullName)

    # Get Skull Info
    try:
        skullData["skullInfo"]=soup.find("span", {"id":"Skull_Info"}).find_next("p").get_text(strip=True)
    except AttributeError:
        skullData["description"]="MISSING"
        print(f"The description for ? is missing",skullName)
    
    # Get Basic Attack Info
    try:
        skullData["basicAttackInfo"]=soup.find("span", {"id":"Basic_Attack_Info"}).find_next("p").get_text(strip=True)
    except AttributeError:
        skullData["description"]="MISSING"
        print(f"The description for ? is missing",skullName)
    
    # Get Passive Skill
    try:
        skullData["passiveSkill"]=soup.find(string=re.compile("Passive Skill")).find_next("li").get_text(strip=True)
    except AttributeError:
        skullData["description"]="MISSING"
        print(f"The description for ? is missing",skullName)

    # Get Swap Skill
    try:
        swapSkillData=soup.find(string=re.compile("Swap Skill")).find_parent("table")
        for tr in swapSkillData.find_all("tr"):
            tds = tr.find_all("td")
            if not tds:
                continue
            if tds[0].get_text(strip=True)=="Skill Name":
                continue
            skullData["swapSkillName"]=tds[0].get_text(strip=True)
            skullData["swapSkillInfo"]=tds[1].get_text(strip=True)
    except AttributeError:
        skullData["description"]="MISSING"
        print(f"The description for ? is missing",skullName)

    # Get Active Skills
    try:
        actSkillData=soup.find(string=re.compile("Activated Skills")).find_parent("table")
        for tr in actSkillData.find_all("tr"):
            tds=tr.find_all("td")
            if not tds:
                continue
            if tds[0].get_text(strip=True)=="Skill Name":
                continue
            skullData["activeSkill"].append({"name":tds[0].get_text(strip=True),"info":tds[1].get_text(strip=True),"cooldown":tds[2].get_text(strip=True)})
    except AttributeError:
        skullData["description"]="MISSING"
        print(f"The description for ? is missing",skullName)

    # Send to database
    print(skullData)
    with open("skullData.json","a") as file:
        file.write(json.dumps(skullData,indent=2))
    with dbcm.Database('skul.db') as db:
        db.execute("INSERT INTO SKULLS (skullName
        ,description
        --continue on
        ) VALUES(?,?)
        ON CONFLICT DO NOTHING;")


if __name__ == '__main__':
    skulls=getSkulls()
    for skull in skulls:
        getSkullData(skull)
