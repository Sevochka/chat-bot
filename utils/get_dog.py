import requests

base_url = "https://shibe.online/api/shibes?count=1&urls=true"


def get_dogy():
    response = requests.get(base_url)
    dogis = response.json()
    return {"dogy": dogis[0]}


exported_functions = [get_dogy]
