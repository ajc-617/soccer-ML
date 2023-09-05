from bs4 import BeautifulSoup

import requests, json

class DataFetcher:

    base_url = json.load(open('../const/metadata.json'))['PL_team_stats_base_url']

    def fetchPLTeamStats(self):
        team_stats_dictionary = {}


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
        
        first_run = True
        #Loop through all rows in for table, then all rows in against table
        #Loop through first time to get the team names to store in the dictionary for future use
        rows = team_for_stats.find("tbody").find_all("tr")
        for cur_row in rows:
            cur_team_name = cur_row.find("th").find("a").string
            team_stats_dictionary[cur_team_name] = {}
                
            
        print(team_stats_dictionary)
        #rows = team_against_stats.find_all("tr")
        #for cur_row in rows:
            



        
        
