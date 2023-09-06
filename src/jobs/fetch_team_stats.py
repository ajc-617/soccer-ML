from bs4 import BeautifulSoup

import requests, json

class DataFetcher:

    base_url = json.load(open('../const/metadata.json'))['PL_team_stats_base_url']

    def fetchAndWritePLTeamStats(self):
        team_stats_for_dictionary = {}


        #Div id for team stats: div_stats_squads_standard_for
        #Div id for opponent stats: div_stats_squads_standard_against

        http_response = requests.get(self.base_url)
        if http_response.status_code != 200:
            raise Exception("Error in fetch PL team stats: response code when making get request was not 200")
        else:
            print("Succesfully fetched PL team stats HTML")

        doc = BeautifulSoup(http_response.text, "html.parser")
        team_for_stats = doc.find("div", {"id": "div_stats_squads_standard_for"})
        team_against_stats = doc.find("div", {"id": "div_stats_squads_standard_against"})
        if team_for_stats is None or team_against_stats is None:
            raise Exception("Error in fetch PL team stats: div names not found for team stat tables")
        
        stat_names = []
        #First get the stats that every team will use
        header_row = team_for_stats.find("thead").find_all("tr")[1].find_all("th")
        #exclude first entry in header row because that's just the squad name
        for entry in header_row[1:]:
            stat_names.append(entry.attrs['aria-label'])
        stat_names[-1] = 'npxG + xAG/90'
            
        #Loop through all rows in for table, then all rows in against table
        #Loop through first time to get the team names to store in the dictionary for future use
        data_rows = team_for_stats.find("tbody").find_all("tr")
        for cur_row in data_rows:
            for index, cur_row_entry in enumerate(cur_row):
                if index == 0: #This will just be a th tag after this one the rest of the row is td entries
                    cur_team_name = cur_row_entry.find("a").string
                    team_stats_for_dictionary[cur_team_name] = {}
                    continue
                team_stats_for_dictionary[cur_team_name][stat_names[index-1]] = cur_row_entry.string
        
        print(len(team_stats_for_dictionary['Arsenal']))
        #Each team should have 31 rows



        
        
