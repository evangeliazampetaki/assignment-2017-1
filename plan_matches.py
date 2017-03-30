import sys
import copy


games = []
unique_players = set()
d_parameter = {}
# read graph file
with open(sys.argv[1], 'r') as graph:
    for line in graph:
        temp_line = line.strip('\n').split(' ')
        # temp_line is a list with 2 elements. E.g. ['a', 'b']
        for player in temp_line:
            unique_players.add(player)
            
            if player in d_parameter.keys():
                d_parameter[player] +=1
            else:
                d_parameter[player] = 1
                
        # Create pairs as tuples. E.g. ('a','b')
        if temp_line[0] > temp_line[1]:
            pair = (temp_line[1], temp_line[0])
        else:
            pair = (temp_line[0], temp_line[1])
        # Add pairs to 'games' list. E.g. [('a','b'), ('a','c')]
        games.append(pair)

games_keep_list = copy.deepcopy(games)

games_keep_list.sort(key=lambda tup: (tup[0], tup[1]))

max_value_key = max(d_parameter)
max_d_value = d_parameter[max_value_key]

games_played_each_day = {}

# According to the assignment we can find solution after 2 * n (or 2 * (n+1)) attempts
# range method second parameter is not inclusive. Thus, we add 1
for game_day in range(0, 2 * (max_d_value + 1) + 1):
    # Each day a number a games will be played. Those will be appended in this list
    # E.g. {0:[('a', 'b'), ('c','d')]} means that the first day (zero-indexed) two games will be played.
    games_played_each_day[game_day] = []
    # We are going to remove items from 'games' list. If it's empty it means we arranged all matches.
    if games:
        # I use games[:] to safely remove element while iterating over the list
        for game in games[:]:
            # The whole strategy is in the following lines. I am checking for each day if each player of a pair(game[0],
            # game[1], plays another game for this specific day. If it does one of the conditionals
            # (x == game[0] or x == game[1] or y == game[0] or y == game[1]), will trigger the list comprehension
            # And check_list will have an element. In this case (if check_list (i.e. has an element)) we should pass
            # That pair (because one of the players plays another game.
            
            # If the check_list is empty (else..), it means both players have not other games arranged.
            # Thus, they can arranged to play this day (games_played_each_day[game_day].append(game)).
            # Following the arrangement we remove that pair for the 'game' list (they have already arranged to play).
            
            # We do the same thing for every day.
            check_list = [(x, y) for x, y in games_played_each_day[game_day]
                          if (x == game[0] or x == game[1] or y == game[0] or y == game[1])]
            if check_list:
                pass
            else:
                games_played_each_day[game_day].append(game)
                games.remove(game)
                
    else:
        # Remove the last day, because it was already created (line 33) and it's empty
        del games_played_each_day[game_day]
        break
# Each pair is unique. Thus, we invert the games_played_each_day dictionary, in which keys were the days
# And values were the list of games played.
match_played_by_day = {}
for day, matches in games_played_each_day.items():
    # Value is a list, so we iterate through it.
    for match in matches:
        match_played_by_day[match] = day

for sorted_game in games_keep_list:
    print("(%s, %s) %d") % (sorted_game[0], sorted_game[1], match_played_by_day[sorted_game])
