import json
import csv
import pandas as pd

class StoreCSV:
    
    def __init__(self) -> None:
        pass
    
    def createCSV(self, league):
        base = '../data'
        for_stats_file = open(f'{base}/{league}_loaded_team_for_data.json')
        against_stats_file = open(f'{base}/{league}_loaded_team_against_data.json')
        scores_file = open(f'{base}/{league}_loaded_scores_data.json')
            
        for_stats = json.load(for_stats_file)
        against_stats = json.load(against_stats_file)
        scores = json.load(scores_file)
        all_scores = []
    
        #Every game score and XG outcome will be a label, so loop through all the games, get the winning team's stats
        for cur_score in scores:
            new_dict = {}
            home_team = cur_score['Home Team']['Name']
            away_team = cur_score['Away Team']['Name']
            for cur_stat in for_stats[home_team]:
                if cur_stat == 'Matches Played' or cur_stat == 'Starts' or cur_stat == 'Minutes' or cur_stat == '90s Played':
                    continue
                new_dict[f'Home for {cur_stat}'] = float(for_stats[home_team][cur_stat])
            for cur_stat in against_stats[home_team]:
                if cur_stat == 'Matches Played' or cur_stat == 'Starts' or cur_stat == 'Minutes' or cur_stat == '90s Played':
                    continue
                new_dict[f'Home against {cur_stat}'] = float(against_stats[home_team][cur_stat])
            for cur_stat in for_stats[away_team]:
                if cur_stat == 'Matches Played' or cur_stat == 'Starts' or cur_stat == 'Minutes' or cur_stat == '90s Played':
                    continue
                new_dict[f'Away for {cur_stat}'] = float(for_stats[home_team][cur_stat])
            for cur_stat in against_stats[away_team]:
                if cur_stat == 'Matches Played' or cur_stat == 'Starts' or cur_stat == 'Minutes' or cur_stat == '90s Played':
                    continue
                new_dict[f'Away against {cur_stat}'] = float(against_stats[away_team][cur_stat])
            
            new_dict['Home Outcome Score'] = float(cur_score['Home Team']['Score'])
            new_dict['Away Outcome Score'] = float(cur_score['Away Team']['Score'])
            new_dict['Home Outcome XG'] = float(cur_score['Home Team']['XG'])
            new_dict['Away Outcome XG'] = float(cur_score['Away Team']['XG'])

            all_scores.append(new_dict)

            pd.DataFrame(all_scores).to_csv(f'{league}.csv', index=False)  
        
