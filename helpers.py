import requests
from urllib.parse import urlencode, uses_relative
import settings
from settings import DEFAULT_REGION, TFT_DEFAULT_REGION
import time
import matplotlib.pyplot as plt

def get_summoner_info(tagline=None, gamename=None, region=settings.DEFAULT_REGION):
    if not tagline:
        tagline = input("Tag Line: ")
    if not gamename:
        gamename = input("Game Name: ")

    params = {'api_key': settings.API_KEY}

    api_url = f"https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gamename}/{tagline}"

    try:
        response = requests.get(api_url, params=urlencode(params))
        response.raise_for_status()
        time.sleep(1)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f'Issues getting summoner data from API: {e}')
        return None

def get_match_ids_by_summoner_puuid(summoner_puuid, matches_count, region = settings.TFT_DEFAULT_REGION):
    params = {'api_key': settings.API_KEY, 'count': matches_count}

    api_url = f"https://{TFT_DEFAULT_REGION}.api.riotgames.com/tft/match/v1/matches/by-puuid/{summoner_puuid}/ids"
    try:
        response = requests.get(api_url, params = urlencode(params))
        response.raise_for_status()
        time.sleep(1)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f'Issues getting summoner match data from API: {e}')
        return None

def player_placements(summoner_puuid, match_id, region = settings.TFT_DEFAULT_REGION):
    params = {'api_key':settings.API_KEY}

    api_url = f"https://{region}.api.riotgames.com/tft/match/v1/matches/{match_id}"

    try:
        response = requests.get(api_url, params = urlencode(params))
        response.raise_for_status()
        time.sleep(1)
        match_data = response.json()
    except requests.exceptions.RequestException as e:
        print(f'Issue getting match data from match id from API: {e}')
        return None

    if summoner_puuid in match_data['metadata']['participants']:
        player_index = match_data['metadata']['participants'].index(summoner_puuid)
    else:
        return None

    player_info = match_data['info']['participants'][player_index]
    return player_info['placement']



def placement_distribution_of_games(tagline, gamename, matches, region=settings.TFT_DEFAULT_REGION):
    summoner = get_summoner_info(tagline, gamename)
    matches = get_match_ids_by_summoner_puuid(summoner['puuid'], matches)

    dist = {}
    for match_id in matches:
        placement = player_placements(summoner['puuid'], match_id)
        if placement not in dist:
            dist[placement] = 1
        else:
            dist[placement] += 1

    return dist

def plot_placement_distribution(dist):
    placements = sorted(dist.keys())
    counts = []
    for placement in placements:
        counts.append(dist[placement])

    plt.figure(figsize=(10, 6))
    plt.bar(placements, counts, color='skyblue')
    plt.xlabel('Placement')
    plt.ylabel('Number of Matches')
    plt.title('Distribution of Placements in TFT Matches')
    plt.xticks(placements)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.show()

def top4_placement_of_games(tagline, gamename, matches, region=settings.TFT_DEFAULT_REGION):
    summoner = get_summoner_info(tagline, gamename)
    matches = get_match_ids_by_summoner_puuid(summoner['puuid'], matches)

    dist = {'top4':0 , 'bot4':0}
    for match_id in matches:
        placement = player_placements(summoner['puuid'], match_id)
        if placement <= 4:
            dist['top4'] += 1
        else:
            dist['bot4'] += 1

    return dist

def plot_top4_placement_distribution(dist):
    placements = sorted(dist.keys())
    counts = []
    for placement in placements:
        counts.append(dist[placement])

    plt.figure(figsize=(10, 6))
    plt.bar(placements, counts, color='skyblue')
    plt.xlabel('Placement')
    plt.ylabel('Number of Matches')
    plt.title('Distribution of Placements in TFT Matches')
    plt.xticks(placements)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.show()