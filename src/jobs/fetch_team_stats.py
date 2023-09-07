from collections.abc import Iterable
from bs4 import BeautifulSoup

import requests, json

class DataFetcher:

    def __init__(self) -> None:
        self.base_url = ""
        self.for_stats_json = ""
        self.against_stats_json = ""
        self.five_leagues = ["PL", "SerieA", "Bundesliga", "Ligue1", "LaLiga"]

    def mainDataFetch(self):
        for league in self.five_leagues:
            self.fetchAndWriteLeagueTeamStats(league)

    def fetchAndWriteLeagueTeamStats(self, league):
        team_stats_for_dictionary = {}
        team_stats_against_dictionary = {}

        #Div id for team stats: div_stats_squads_standard_for
        #Div id for opponent stats: div_stats_squads_standard_against

        match league:
            case "PL":
                self.base_url = json.load(open('../const/metadata.json'))['PL_team_stats_base_url']
                self.for_stats_json = "../data/PL_loaded_team_for_data.json"
                self.against_stats_json = "../data/PL_loaded_team_against_data.json"
            case "SerieA":
                self.base_url = json.load(open('../const/metadata.json'))['SerieA_team_stats_base_url']
                self.for_stats_json = "../data/SerieA_loaded_team_for_data.json"
                self.against_stats_json = "../data/SerieA_loaded_team_against_data.json"
            case "Bundesliga":
                self.base_url = json.load(open('../const/metadata.json'))['Bundesliga_team_stats_base_url']
                self.for_stats_json = "../data/Bundesliga_loaded_team_for_data.json"
                self.against_stats_json = "../data/Bundesliga_loaded_team_against_data.json"    
            case "Ligue1":
                self.base_url = json.load(open('../const/metadata.json'))['Ligue1_team_stats_base_url']
                self.for_stats_json = "../data/Ligue1_loaded_team_for_data.json"
                self.against_stats_json = "../data/Ligue1_loaded_team_against_data.json"
            case "LaLiga":
                self.base_url = json.load(open('../const/metadata.json'))['LaLiga_team_stats_base_url']
                self.for_stats_json = "../data/LaLiga_loaded_team_for_data.json"
                self.against_stats_json = "../data/LaLiga_loaded_team_against_data.json"

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
        #For some reason, npXg + xAG has the same aria label as the same stat but per 90 minutes, so need this
        stat_names[-1] = 'npxG + xAG/90'
            
        #Loop through all rows in for table, then all rows in against table
        #Loop through first time to get the team names to store in the dictionary for future use
        data_for_rows = team_for_stats.find("tbody").find_all("tr")
        data_against_rows = team_against_stats.find("tbody").find_all("tr")
        for cur_for_row, cur_against_row in zip(data_for_rows, data_against_rows):
            for index, (cur_for_row_entry, cur_against_row_entry) in enumerate(zip(cur_for_row, cur_against_row)):
                if index == 0: #This will just be a th tag after this one the rest of the row is td entries
                    cur_team_name = cur_for_row_entry.find("a").string
                    team_stats_for_dictionary[cur_team_name] = {}
                    team_stats_against_dictionary[cur_team_name] = {}
                    continue
                team_stats_for_dictionary[cur_team_name][stat_names[index-1]] = cur_for_row_entry.string
                team_stats_against_dictionary[cur_team_name][stat_names[index-1]] = cur_against_row_entry.string
            

        team_for_stats_file = open(self.for_stats_json, "w")
        team_against_stats_file = open(self.against_stats_json, "w")
        json.dump(team_stats_for_dictionary, team_for_stats_file, indent=2)
        json.dump(team_stats_against_dictionary, team_against_stats_file, indent=2)




        
        
