from bs4 import BeautifulSoup

import requests, json

class DataFetcher:

    def __init__(self) -> None:
        self.base_url = ""
        self.for_stats_json = ""
        self.against_stats_json = ""
        self.scores_json = ""
        self.five_leagues = ["PL", "SerieA", "Bundesliga", "Ligue1", "LaLiga"]

    #def mainDataFetch(self):
        #for league in self.five_leagues:
        #    self.fetchAndWriteLeagueTeamStats(league)
    #    self.fetchAndWriteLeagueScores("PL")

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
            raise Exception(f"Error in fetch {league} team stats: response code when making get request was not 200")
        else:
            print("Succesfully fetched team stats HTML")

        doc = BeautifulSoup(http_response.text, "html.parser")
        team_for_stats = doc.find("div", {"id": "div_stats_squads_standard_for"})
        team_against_stats = doc.find("div", {"id": "div_stats_squads_standard_against"})
        if team_for_stats is None or team_against_stats is None:
            raise Exception(f"Error in fetch {league} team stats: div names not found for team stat tables")
        
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
        #iterate throw for and against rows at the same time
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

    def fetchAndWriteLeagueScores(self,league):
        table_ids = {'PL': '9', 'SerieA': '11', 'Bundesliga': '20', 'Ligue1': '13', 'LaLiga': '12'}


        match league:
            case "PL":
                self.base_url = json.load(open('../const/metadata.json'))['PL_scores_base_url']
                self.scores_json = "../data/PL_loaded_scores_data.json"
            case "SerieA":
                self.base_url = json.load(open('../const/metadata.json'))['SerieA_scores_base_url']
                self.scores_json = "../data/SerieA_loaded_scores_data.json"
            case "Bundesliga":
                self.base_url = json.load(open('../const/metadata.json'))['Bundesliga_scores_base_url']  
                self.scores_json = "../data/Bundesliga_loaded_scores_data.json"
            case "Ligue1":
                self.base_url = json.load(open('../const/metadata.json'))['Ligue1_scores_base_url']
                self.scores_json = "../data/Ligue1_loaded_scores_data.json"
            case "LaLiga":
                self.base_url = json.load(open('../const/metadata.json'))['LaLiga_scores_base_url']
                self.scores_json = "../data/LaLiga_loaded_scores_data.json"

        http_response = requests.get(self.base_url)
        if http_response.status_code != 200:
            raise Exception(f"Error in {league} fetch scores: response code when making get request was not 200")
        else:
            print("Succesfully fetched scores HTML")

        doc = BeautifulSoup(http_response.text, "html.parser")
        score_table = doc.find("table", {"id": f"sched_2022-2023_{table_ids[league]}_1"})
        rows = score_table.find("tbody").find_all("tr")
        all_games = []
        for cur_row in rows:
            #this means this row has nothing in it (a divider row basically)
            try:  
                #If class doesn't exist, that means we have an actual data row, so go to except block
                if cur_row.attrs['class'] == "spacer partial_table result_all":
                    continue
            except:
                cur_game_dict = {}
                cur_game_dict['Home Team'] = {}
                cur_game_dict['Away Team'] = {}
                entries = cur_row.find_all("td")
                #Inside the row, the home team
                cur_game_dict['Home Team']['Name'] = entries[3].find("a").string
                cur_game_dict['Home Team']['XG'] = entries[4].string
                #this string is formatted like '2-1' for example
                score_string = list(entries[5].find("a").string)
                cur_game_dict['Home Team']['Score'] = score_string[0]
                cur_game_dict['Away Team']['Name'] = entries[7].find("a").string
                cur_game_dict['Away Team']['XG'] = entries[6].string
                cur_game_dict['Away Team']['Score'] = score_string[2]
                all_games.append(cur_game_dict)
            
        league_scores_file = open(self.scores_json, "w")
        json.dump(all_games, league_scores_file, indent=2)

                




        
        
