from jobs.fetch_team_stats import DataFetcher
from jobs.create_csv import StoreCSV
import os
from model.ml_dataset import SoccerDataset
import csv
import torch
from torch.utils.data import DataLoader


def main_function():
    leagues = ['PL', 'SerieA', 'Bundesliga', 'Ligue1', 'LaLiga']
    #test_obj = StoreCSV()
    #for league in leagues:
    #    test_obj.createCSV(league)
    #    os.rename(f'{league}.csv', f'../csv/{league}.csv')
    csv_file = open('../csv/PL.csv', 'r')
    dict_reader = csv.DictReader(csv_file)
    games = list(dict_reader)

    soccer_dataset = SoccerDataset('../csv/PL.csv', root_dir='/')
    sample = soccer_dataset[0]
    print(sample['stats'].shape)
    print(sample['scores'].shape)
    dataloader = DataLoader(soccer_dataset, batch_size=32)
    for i_batch, sample_batched in enumerate(dataloader):
        print(i_batch, sample_batched['stats'].size(),
            sample_batched['scores'].size())

if __name__ == "__main__":
    main_function()