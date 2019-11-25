# original author : https://github.com/vaastav
# source: https://github.com/vaastav/Fantasy-Premier-League

from parsers import *
from cleaners import *
from getters import *
from collector import collect_gw, merge_gw
import os


def parse_data():
    '''
    Parse and store all the data
    '''

    print("Getting data")
    data = get_data()

    if not os.path.exists('data'):
        os.mkdir('data')

    with open(f'data/gameweeks.json', 'w', encoding='utf-8') as f:
        json.dump(data['events'], f, ensure_ascii=True, indent=2)

    season = '2019-20'
    base_filename = 'data/' + season + '/'
    
    print("Parsing summary data")
    parse_players(data["elements"], base_filename)
    
    gw_num = 0
    events = data["events"]
    for event in events:
        if event["is_current"] == True:
            gw_num = event["id"]
    
    print("Cleaning summary data")
    clean_players(base_filename + 'players_raw.csv', base_filename)
    
    print("Getting fixtures data")
    fixtures(base_filename)
    
    if gw_num == 0:
        print("Getting teams data")
        parse_team_data(data["teams"], base_filename)
    
    print("Extracting player ids")
    id_players(base_filename + 'players_raw.csv', base_filename)
    
    player_ids = get_player_ids(base_filename)
    num_players = len(data["elements"])
    player_base_filename = base_filename + 'players/'
    gw_base_filename = base_filename + 'gws/'
    
    print("Extracting player specific data")
    for i,name in player_ids.items():
        player_data = get_individual_player_data(i)
        parse_player_history(player_data["history_past"], player_base_filename, name, i)
        parse_player_gw_history(player_data["history"], player_base_filename, name, i)


def fixtures(base_filename):
    data = get_fixtures_data()
    parse_fixtures(data, base_filename)


def main():
    parse_data()


if __name__ == "__main__":
    start = time.time()
    main()
    finish = time.time()
    print(f'Took {round(finish-start, 2)} seconds.')
