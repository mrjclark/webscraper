import requests
from bs4 import BeautifulSoup

# API endpoint and parameters
uri = "https://skul.fandom.com/api.php"
params = {
    "action": "parse",
    "page": "Skulls",
    "prop": "text",
    "format": "json"
}
headers = {"User-Agent": "SkulCrawler/1.0"}

# Make the request
response = requests.get(uri, params=params, headers=headers)
data = response.json()

# Extract the HTML text from the JSON
html = data["parse"]["text"]["*"]

# Create a BeautifulSoup object
soup = BeautifulSoup(html, "html.parser")

# Define exclusions
exclude = {"Balrog", "Harpy", "Guard Captain", "Slime"}

# Loop through table cells and list items
for td in soup.find_all("td"):
    for li in td.find_all("li"):
        if li.a and "title" in li.a.attrs:
            skull_name = li.a["title"]
            if skull_name not in exclude:
                print(skull_name)
