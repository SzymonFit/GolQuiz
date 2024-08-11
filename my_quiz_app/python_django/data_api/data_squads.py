import requests
import json
from django.conf import settings


def football_squads():
    url = "https://api-football-v1.p.rapidapi.com/v3/players/squads"

    queries = [
        # {"team": "529"}, # Barcelona
        # {"team": "541"}, # Real Madrid
        # {"team": "530"}, # Atletico Madrid
        # {"team": "536"}, # Sevilla

        # {"team": "33"}, # Machester United
        # {"team": "50"}, # Manchester City
        # {"team": "40"}, # Liverpool
        # {"team": "49"}, # Chelsea
        # {"team": "42"}, # Arsenal
        # {"team": "47"}, # Tottenham

        # {"team": "157"}, # Bayern Munich
        # {"team": "165"}, # Borussia Dortmund
        # {"team": "173"}, # RB Leipzig
        # {"team": "168"}, # Bayer Leverkusen

        # {"team": "85"}, # PSG
        # {"team": "80"}, # Lyon
        # {"team": "91"}, # Monaco
        # {"team": "81"}, # Marseille
    
        # {"team": "496"}, # Juventus
        # {"team": "505"}, # Inter Milan
        # {"team": "489"}, # AC Milan
        # {"team": "492"}, # Napoli

        # {"team": "339"}, # Legia Warsaw
        # {"team": "347"}, # Lech Poznan
        # {"team": "336"}, # Jagiellonia Bialystok


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
    with open('squads.json', 'w') as file:
        json.dump(all_data, file, indent=4)

football_squads()


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
file_path = 'squads.json'

# Wczytanie danych z pliku JSON
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Dekodowanie zakodowanych znaków Unicode
decoded_data = decode_unicode(data)

# Zapisanie przetworzonych danych do tego samego pliku JSON
with open(file_path, 'w', encoding='utf-8') as file:
    json.dump(decoded_data, file, ensure_ascii=False, indent=4)

print(f"Przetworzone dane zostały zapisane do {file_path}")