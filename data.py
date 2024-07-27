from django.conf import settings
import requests
import json


def leagues_by_country_name():
    url = "https://api-football-v1.p.rapidapi.com/v3/leagues"

    queries = [
        # {"country": "England", "name": "Premier League"},
        # {"country": "Spain", "name": "La Liga"},
        # {"country": "Italy", "name": "Serie A"},
        # {"country": "Germany", "name": "Bundesliga"},
        # {"country": "France", "name": "Ligue 1"},
        # {"country": "Poland", "name": "Ekstraklasa"}

    ]

    headers = {
        "x-rapidapi-key": settings.API_KEY,
        "x-rapidapi-host": settings.API_HOST
    }
    for query in queries:
        response = requests.get(url, headers=headers, params=query)
        data = response.json()  # Otrzymanie danych w formacie JSON
        print(data)
        
        # Utworzenie nazwy pliku na podstawie nazwy ligi
        file_name = f"leagues_by_country_{query['country']}_{query['name'].replace(' ', '')}.json"
        
        # Zapisanie danych do pliku JSON
        with open(file_name, 'w') as file:
            json.dump(data, file, indent=4)

# Wywołanie funkcji
leagues_by_country_name()