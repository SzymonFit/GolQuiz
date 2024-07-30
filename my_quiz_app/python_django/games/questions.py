import json
import random
from django.conf import settings
from pathlib import Path
from datetime import datetime, timedelta

def load_questions(game_mode):
    file_paths = {
        'mode1': [Path(settings.BASE_DIR) / "all_json's/top_scorers/top_scorers.json"],
        'mode2': [
            Path(settings.BASE_DIR) / "all_json's/squads/squads.json",
            Path(settings.BASE_DIR) / "all_json's/leagues/leagues_by_country_England_PremierLeague.json",
            Path(settings.BASE_DIR) / "all_json's/leagues/leagues_by_country_France_Ligue1.json",
            Path(settings.BASE_DIR) / "all_json's/leagues/leagues_by_country_Germany_Bundesliga.json",
            Path(settings.BASE_DIR) / "all_json's/leagues/leagues_by_country_Italy_SerieA.json",
            Path(settings.BASE_DIR) / "all_json's/leagues/leagues_by_country_Poland_Ekstraklasa.json",
            Path(settings.BASE_DIR) / "all_json's/leagues/leagues_by_country_Spain_LaLiga.json",
        ]
    }
    if game_mode not in file_paths:
        raise ValueError("Invalid game mode")
    
    questions = []
    for file_path in file_paths[game_mode]:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if isinstance(data, list):
                questions.extend(data)
            else:
                questions.append(data)
    return questions

def get_league_name(league_id):
    leagues = {
        "39": "Premier League",
        "140": "La Liga",
        "135": "Serie A",
        "78": "Bundesliga",
        "61": "Ligue 1",
        "106": "Ekstraklasa",
    }
    return leagues.get(str(league_id), "Unknown League")

def get_ordinal_suffix(n):
    if 10 <= n % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return suffix

def generate_date_options(correct_date):
    date = datetime.strptime(correct_date, "%Y-%m-%d")
    options = [correct_date]
    while len(options) < 4:  # Ensure there are only 4 options
        random_date = date + timedelta(days=random.randint(-30, 30))
        option = random_date.strftime("%Y-%m-%d")
        if option not in options:
            options.append(option)
    random.shuffle(options)
    return options

def generate_squad_question(record):
    team = record['response'][0]['team']['name']
    players = [player for player in record['response'][0]['players'] if player['number'] is not None]
    player = random.choice(players)

    questions = []

    if random.choice([True, False]):
        question_text = f"What is the number of {player['name']} in {team}?"
        correct_answer = str(player['number'])
        options = [correct_answer]
        while len(options) < 4:
            option = str(random.randint(1, 99))
            if option not in options:
                options.append(option)
        random.shuffle(options)
        questions.append({
            "question": question_text,
            "correct_answer": correct_answer,
            "options": options
        })
    else:
        question_text = f"What position does {player['name']} play in {team}?"
        correct_answer = player['position']
        questions.append({
            "question": question_text,
            "correct_answer": correct_answer,
            "options": None
        })

    return questions[0]  # Return a single question dictionary instead of a list

def generate_mode1_question(record, place):
    league_id = record['parameters']['league']
    season = record['parameters']['season']
    league_name = get_league_name(league_id)
    top_scorer = record['response'][place]
    place_ordinal = f"{place + 1}{get_ordinal_suffix(place + 1)}"

    question_type = random.choice(['name', 'goals', 'place'])

    if question_type == 'name' and place == 0:
        question_text = f"Who was the top scorer in the {season} {league_name} season?"
        correct_answer = top_scorer['player']['name']
    elif question_type == 'goals':
        question_text = f"Who scored {top_scorer['statistics'][0]['goals']['total']} goals in the {season} {league_name} season?"
        correct_answer = top_scorer['player']['name']
    elif question_type == 'place' and place > 0:
        question_text = f"Who was the {place_ordinal} top scorer in the {season} {league_name} season?"
        correct_answer = top_scorer['player']['name']
    else:
        return generate_mode1_question(record, place)  # Retry to avoid asking the same question type for the top scorer

    return {
        "question": question_text,
        "correct_answer": correct_answer,
        "league": league_name,
        "season": season,
        "player_name": top_scorer['player']['name'],
        "goals": top_scorer['statistics'][0]['goals']['total'],
        "place": place + 1
    }

def generate_mode2_question(record):
    if isinstance(record['response'], list) and 'seasons' in record['response'][0]:
        league_id = record['response'][0]['league']['id']
        league_name = record['response'][0]['league']['name']
        season_info = random.choice(record['response'][0]['seasons'])
        season_year = season_info['year']
        question_type = random.choice(['start_date', 'end_date'])

        if question_type == 'start_date':
            question_text = f"When did the {season_year} {league_name} season start?"
            correct_answer = season_info['start']
        else:
            question_text = f"When did the {season_year} {league_name} season end?"
            correct_answer = season_info['end']

        options = generate_date_options(correct_answer)
        return {
            "question": question_text,
            "correct_answer": correct_answer,
            "options": options
        }
    elif isinstance(record['response'], list) and 'team' in record['response'][0]:
        return generate_squad_question(record)
    else:
        raise ValueError("Invalid record structure for mode2")

def generate_question(record, place, game_mode):
    if game_mode == 'mode1':
        return generate_mode1_question(record, place)
    elif game_mode == 'mode2':
        return generate_mode2_question(record)
    elif game_mode == 'mode3':
        if 'seasons' in record['response'][0]:
            return generate_question(record, place, 'mode2')
        else:
            return generate_question(record, place, 'mode1')
    else:
        raise ValueError("Invalid game mode")

def get_random_question(game_mode):
    if game_mode == 'mode3':
        chosen_mode = random.choice(['mode1', 'mode2'])
        questions = load_questions(chosen_mode)
        record = random.choice(questions)
        place = random.randint(0, 9)
        return generate_question(record, place, chosen_mode)
    else:
        questions = load_questions(game_mode)
        record = random.choice(questions)
        place = random.randint(0, 9)
        return generate_question(record, place, game_mode)

def check_answer(question, answer):
    correct_answer = question['correct_answer'].strip().lower()
    user_answer = answer.strip().lower()
    return correct_answer == user_answer
