# original author : https://github.com/vaastav
# source: https://github.com/vaastav/Fantasy-Premier-League

from getters import *
from parsers import *
import sys
import os

sys.path.append('../')
import variables


def main():
    # if len(sys.argv) != 2:
        # print("Usage: python teams_scraper.py <team_id>. Eg: python teams_scraper.py 5000")
        # sys.exit(1)
    
    season = "19_20"
    output_folder = "data/team_data"
    # team_id = int(sys.argv[1])
    team_id = variables.TEAM_ID
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    summary = get_entry_data(team_id)
    personal_data = get_entry_personal_data(team_id)
    num_gws = len(summary["current"])
    gws = get_entry_gws_data(team_id, num_gws)
    parse_entry_history(summary, output_folder)
    parse_entry_leagues(personal_data, output_folder)
    parse_gw_entry_history(gws, output_folder)


if __name__ == '__main__':
    start = time.time()
    main()
    finish = time.time()
    print(f'Took {round(finish-start, 2)} seconds.')
