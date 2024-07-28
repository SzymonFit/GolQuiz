import json
import random
from django.conf import settings
from pathlib import Path

def load_questions():
    file_path = Path(settings.BASE_DIR) / "all_json's/top_scorers/top_scorers.json"
    with open(file_path, 'r', encoding='utf-8') as file:
        questions = json.load(file)
    return questions

def get_league_name(league_id):
    leagues = {
        "39": "Premier League",
        "140": "La Liga",
        "135": "Serie A",
        "78": "Bundesliga"
        # Dodaj inne ligi w razie potrzeby
    }
    return leagues.get(str(league_id), "Unknown League")

def get_ordinal_suffix(n):
    if 10 <= n % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return suffix

def generate_question(record, place):
    league_id = record['parameters']['league']
    season = record['parameters']['season']
    league_name = get_league_name(league_id)
    top_scorer = record['response'][place]
    place_ordinal = f"{place + 1}{get_ordinal_suffix(place + 1)}"

    question_type = random.choice(['name', 'goals', 'place'])

    if place == 0 and question_type == 'name':

        question_text = f"Who was the top scorer in the {season} {league_name} season?"
        correct_answer = top_scorer['player']['name']
    elif question_type == 'goals':
        question_text = f"Who scored {top_scorer['statistics'][0]['goals']['total']} goals in the {season} {league_name} season?"
        correct_answer = top_scorer['player']['name']
    else:
        question_text = f"Who was the {place_ordinal} top scorer in the {season} {league_name} season?"
        correct_answer = top_scorer['player']['name']

    return {
        "question": question_text,
        "correct_answer": correct_answer,
        "league": league_name,
        "season": season,
        "player_name": top_scorer['player']['name'],
        "goals": top_scorer['statistics'][0]['goals']['total'],
        "place": place + 1  
    }

def get_random_question():
    questions = load_questions()
    record = random.choice(questions)

    place = random.randint(0, 9) 

    return generate_question(record, place)

def check_answer(question, answer):
    correct_answer = question['correct_answer'].strip().lower()
    user_answer = answer.strip().lower()
    return correct_answer == user_answer
