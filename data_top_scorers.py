import requests
import json
from django.conf import settings


def top_scorers():
    url = "https://api-football-v1.p.rapidapi.com/v3/players/topscorers"

    queries = [
        # {"league":"39","season":"2015"}, # Premier League
        # {"league":"39","season":"2016"}, # Premier League
        # {"league":"39","season":"2017"}, # Premier League
        # {"league":"39","season":"2018"}, # Premier League
        # {"league":"39","season":"2019"}, # Premier League
        # {"league":"39","season":"2020"}, # Premier League
        # {"league":"39","season":"2021"}, # Premier League
        # {"league":"39","season":"2022"}, # Premier League
        # {"league":"39","season":"2023"}, # Premier League
        # {"league":"39","season":"2024"}, # Premier League

        # {"league":"140","season":"2015"}, # La Liga
        # {"league":"140","season":"2016"}, # La Liga
        # {"league":"140","season":"2017"}, # La Liga
        # {"league":"140","season":"2018"}, # La Liga
        # {"league":"140","season":"2019"}, # La Liga
        # {"league":"140","season":"2020"}, # La Liga
        # {"league":"140","season":"2021"}, # La Liga
        # {"league":"140","season":"2022"}, # La Liga
        # {"league":"140","season":"2023"}, # La Liga
        # {"league":"140","season":"2024"}, # La Liga

        # {"league":"135","season":"2015"}, # Serie A
        # {"league":"135","season":"2016"}, # Serie A
        # {"league":"135","season":"2017"}, # Serie A
        # {"league":"135","season":"2018"}, # Serie A
        # {"league":"135","season":"2019"}, # Serie A
        # {"league":"135","season":"2020"}, # Serie A
        # {"league":"135","season":"2021"}, # Serie A
        # {"league":"135","season":"2022"}, # Serie A
        # {"league":"135","season":"2023"}, # Serie A
        # {"league":"135","season":"2024"}, # Serie A


    ]

    headers = {
        "x-rapidapi-key": settings.API_KEY,
        "x-rapidapi-host": settings.API_HOST
    }
    all_data = []

    for query in queries:
        response = requests.get(url, headers=headers, params=query)
        data = response.json()  # Otrzymanie danych w formacie JSON
        print(data)
        all_data.append(data)  # Dodanie danych do listy all_data
    
    # Zapisanie wszystkich danych do jednego pliku JSON
    with open('top_scorers.json', 'w') as file:
        json.dump(all_data, file, indent=4)


# Wywołanie funkcji
top_scorers()


def decode_unicode(data):
    if isinstance(data, dict):
        return {key: decode_unicode(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [decode_unicode(item) for item in data]
    elif isinstance(data, str):
        return bytes(data, "utf-8").decode("unicode_escape").encode("latin1").decode("utf-8")
    else:
        return data

# Ścieżka do pliku JSON
file_path = 'top_scorers.json'

# Wczytanie danych z pliku JSON
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Dekodowanie zakodowanych znaków Unicode
decoded_data = decode_unicode(data)

# Zapisanie przetworzonych danych do tego samego pliku JSON
with open(file_path, 'w', encoding='utf-8') as file:
    json.dump(decoded_data, file, ensure_ascii=False, indent=4)

print(f"Przetworzone dane zostały zapisane do {file_path}")