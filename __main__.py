from helpers import (get_summoner_info, get_match_ids_by_summoner_puuid, player_placements,
                     placement_distribution_of_games, plot_placement_distribution,top4_placement_of_games
                     ,plot_top4_placement_distribution)


tagline = '0610'
gamename = 'Dripzz'

summoner = get_summoner_info(tagline, gamename)

print(summoner)
print(summoner['puuid'])

summoner_match_ids = get_match_ids_by_summoner_puuid(summoner['puuid'], 20)
print(summoner_match_ids)


dist = placement_distribution_of_games(summoner['tagLine'], summoner['gameName'],20)
print("Placement Distribution:", dist)

plot_placement_distribution(dist)

dist = top4_placement_of_games(summoner['tagLine'], summoner['gameName'],20)
print("Top 4 Placement Distribution:", dist)

plot_top4_placement_distribution(dist)