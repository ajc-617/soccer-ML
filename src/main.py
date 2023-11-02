from jobs.fetch_team_stats import DataFetcher
from jobs.create_csv import StoreCSV
import os


def main_function():
    leagues = ['PL', 'SerieA', 'Bundesliga', 'Ligue1', 'LaLiga']
    test_obj = StoreCSV()
    for league in leagues:
        test_obj.createCSV(league)
        os.rename(f'{league}.csv', f'../csv/{league}.csv')

if __name__ == "__main__":
    main_function()