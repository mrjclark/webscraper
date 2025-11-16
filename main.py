import requests
from bs4 import BeautifulSoup
import sqlite3
import time
import getSkullList
from dbcm import Database
import dbSetup

# Set database if not done yet
dbSetup.dbSetup('skul.db')

# API endpoint
URI = "https://skul.fandom.com/api.php"
HEADERS = {"User-Agent": "SkulCrawler/1.0"}

# Example skull list (replace with your crawler output)
skull_names = getSkullList.main() 

# Function to fetch and parse skull page
def fetch_skull_data(skull_name):
    params = {
        "action": "parse",
        "page": skull_name.replace(" ","_"),
        "prop": "text",
        "format": "json"
    }
    resp = requests.get(URI, params=params, headers=HEADERS)
    if not resp.ok:
        return None

    html = resp.json()["parse"]["text"]["*"]
    soup = BeautifulSoup(html, "html.parser")

    # Example parsing logic (depends on wiki infobox structure)
    infobox = soup.find("table", {"class": "infobox"})
    if not infobox:
        return None

    data = {"name": skull_name}

    # Extract fields from infobox rows
    for row in infobox.find_all("tr"):
        header = row.find("th")
        value = row.find("td")
        if not header or not value:
            continue
        key = header.text.strip().lower()
        val = value.text.strip()

        if "rarity" in key:
            data["rarity"] = val
        elif "type" in key:
            data["skull_type"] = val
        elif "damage" in key:
            data["damage_type"] = val
        elif "passive" in key:
            data["passive_skill"] = val
        elif "swap" in key:
            if "swap_skill1" not in data:
                data["swap_skill1"] = val
            else:
                data["swap_skill2"] = val
        elif "skill" in key:
            # Collect all skills into lists
            if "skill_names" not in data:
                data["skill_names"] = []
                data["skill_descriptions"] = []
                data["skill_cooldowns"] = []
            data["skill_names"].append(header.text.strip())
            data["skill_descriptions"].append(val)
            # Cooldowns may be embedded in val or separate cell

    # Flatten lists into strings for SQLite
    for field in ["skill_names", "skill_descriptions", "skill_cooldowns"]:
        if field in data:
            data[field] = "; ".join(data[field])

    return data

# Loop through skulls and insert into DB
for skull in skull_names:
    skull_data = fetch_skull_data(skull)
    if skull_data:
        cur.execute("""
        INSERT OR REPLACE INTO skulls
        (name, rarity, skull_type, damage_type, passive_skill,
         swap_skill1, swap_skill2, skill_names, skill_descriptions, skill_cooldowns)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            skull_data.get("name"),
            skull_data.get("rarity"),
            skull_data.get("skull_type"),
            skull_data.get("damage_type"),
            skull_data.get("passive_skill"),
            skull_data.get("swap_skill1"),
            skull_data.get("swap_skill2"),
            skull_data.get("skill_names"),
            skull_data.get("skill_descriptions"),
            skull_data.get("skill_cooldowns")
        ))
        conn.commit()
    time.sleep(1)  # polite delay

conn.close()
