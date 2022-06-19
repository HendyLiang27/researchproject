import time

import pandas as pd
import os
import json
import schedule

# Slark has hero id 93
# Hurricane Pike has id 263

# Wanted game modes:
# All pick (1)
# Captains mode (2)
# All draft (22)

# Wanted lobby types:
# Normal (1)
# Tournament (2)
# Ranked team mm (5)
# Ranked solo mm (6)
# Ranked (7)


# The endpoint gives all balanced game modes and lobby types.

# This has to be changed on every re-boot of the script to the most recent one
last_match_id = 6558407708

# Same for this
current_index = 26764
match_data = pd.read_csv('match_df.csv')


def hurricane_pike_in_inventory(player):
    return player['backpack_0'] == 263 or player['backpack_1'] == 263 or player['backpack_2'] == 263 or \
           player['item_0'] == 263 or player['item_1'] == 263 or player['item_2'] == 263 or \
           player['item_3'] == 263 or player['item_4'] == 263 or player['item_5'] == 263


def extractMatchInfo(data):
    '''
    A function used to extract info from string data of one match into dataframes.

    INPUT:
    data - data of one match in dictionary (originally obtained from https://api.opendota.com/api/publicMatches)

    OUTPUT:
    arr - a list of match information: match_id, time, game_mode,
    '''

    arr = []

    # Save match_id
    arr.append(data['match_id'])

    # Save game_mode. In this exercise, we are looking for matches with game_mode 2
    arr.append(data['game_mode'])

    # Save lobby_type
    arr.append(data['lobby_type'])

    # Save picks for both teams: team radiant goes first
    radiant = [int(i) for i in data['radiant_team'].split(",")]
    dire = [int(i) for i in data['dire_team'].split(",")]
    arr.extend(radiant)
    arr.extend(dire)

    # Save result: radiant_win
    arr.append(data['radiant_win'])

    return arr


def gather_matches():
    global last_match_id
    calls_made = 0
    while calls_made < 60:
        if last_match_id is None:
            os.system('curl https://api.opendota.com/api/publicMatches > publicMatches.json')
        else:
            os.system(
                'curl https://api.opendota.com/api/publicMatches?less_than_match_id={} > publicMatches.json'.format(
                    last_match_id))
        calls_made += 1
        with open('publicMatches.json') as f:
            data = json.load(f)
            if 'error' in data:
                return

        df = []
        for m in data:
            arr = extractMatchInfo(m)
            df.append(arr)

        pd.DataFrame(df).drop_duplicates(subset=[0], inplace=True, keep='last')
        df = pd.DataFrame(df)
        df.rename(columns={0: "match_id", 1: "game_mode", 2: "lobby_type",
                           3: "radiant_1", 4: "radiant_2", 5: "radiant_3", 6: "radiant_4", 7: "radiant_5",
                           8: "dire_1", 9: "dire_2", 10: "dire_3", 11: "dire_4", 12: "dire_5", 13: "radiant_win"},
                  inplace=True)
        df['slark_found'] = df['radiant_1'].eq(93) | df['radiant_2'].eq(93) | df['radiant_3'].eq(93) | df[
            'radiant_4'].eq(93) | \
                            df['radiant_5'].eq(93) | df['dire_1'].eq(93) | df['dire_1'].eq(93) | df['dire_1'].eq(93) | \
                            df['dire_1'].eq(93) | df['dire_1'].eq(93)
        df['radiant_slark'] = df['radiant_1'].eq(93) | df['radiant_2'].eq(93) | df['radiant_3'].eq(93) | \
                              df['radiant_4'].eq(93) | df['radiant_5'].eq(93)
        df.to_csv('match_df.csv', mode='a', index=False, header=False)
        last_match_id = df.iloc[-1, 0]
    return

def gather_match_data():
    global current_index
    calls_made = 0
    while calls_made < 60:
        row = match_data.iloc[current_index]
        os.system('curl https://api.opendota.com/api/matches/{} > logfile.json'.format(row['match_id']))
        with open('logfile.json', "r+", encoding="utf-8") as f:
            if f is None:
                return
            data = json.load(f)
            if data is None or 'error' in data:
                return
            players = data['players']
            bought_hurricane_pike = list(map(lambda x: hurricane_pike_in_inventory(x), players))
            arr_radiant = [data['radiant_win'], any(bought_hurricane_pike[5:]), row['match_id'], current_index]
            df_radiant = pd.DataFrame(arr_radiant).rename({0: 'win', 1: 'enemy_bought_hurricane_pike', 2: 'match_id', 3: 'index'}).T
            arr_dire = [not data['radiant_win'], any(bought_hurricane_pike[:5]), row['match_id'], current_index]
            df_dire = pd.DataFrame(arr_dire).rename({0: 'win', 1: 'enemy_bought_hurricane_pike', 2: 'match_id', 3: 'index'}).T
            df_radiant.to_csv('hurricane_pike.csv', mode='a', index=False, header=False)
            df_dire.to_csv('hurricane_pike.csv', mode='a', index=False, header=False)
            if row['slark_found']:
                if row['radiant_slark']:
                    df_radiant.to_csv('slark_hurricane_pike.csv', mode='a', index=False, header=False)
                else:
                    df_dire.to_csv('slark_hurricane_pike.csv', mode='a', index=False, header=False)
        current_index += 1
    return

# This for getting details about matches
schedule.every().minute.do(gather_match_data)

# This for getting match ids
# schedule.every().minute.do(gather_matches)

gather_match_data()
while True:
    schedule.run_pending()
    time.sleep(1)

