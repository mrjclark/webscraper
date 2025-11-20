
def url():
     return "https://skul.fandom.com/api.php"

def headers():
    header =  {"User-Agent": "SkulCrawler/1.0"}
    return header

def params(page):
    params = {
        "action": "parse",
        "page": page.replace(" ","_"),
        "prop": "text",
        "format": "json"
    }
    return params
