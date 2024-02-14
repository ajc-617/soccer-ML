from jobs.fetch_team_stats import DataFetcher
from jobs.create_csv import StoreCSV
from model.ml_perceptron import Perceptron
from model.ml_mlp import MultiLayerPerceptron
import os
from model.ml_dataset import SoccerDataset
from model.ml_training_testing import TrainingTesting
import csv
import torch
from torch.utils.data import DataLoader
import torchvision
import numpy as np
import tensorflow as tf


def main_function():
    

    leagues = ['PL', 'SerieA', 'Bundesliga', 'Ligue1', 'LaLiga']
    test_obj = StoreCSV()
    #This is code 
    #for league in leagues:
    #    test_obj.createCSV(league)
    #os.rename(f'{league}.csv', f'../csv/{league}.csv')
    transform_to_float = tensor_to_float32
    soccer_dataset = SoccerDataset('../csv/PL.csv', root_dir='/', transform=transform_to_float)

    dataloader = DataLoader(soccer_dataset, batch_size=4)
    #3 possible output values:
    test_MLP = MultiLayerPerceptron(108, 3)
    #For multiclass classification
    loss_fn = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(test_MLP.parameters(), lr=0.0001, weight_decay=0.07)
    training_obj = TrainingTesting()
    training_obj.training(dataloader, 1000, loss_fn, optimizer, test_MLP)

    PL_results =  next(iter(DataLoader(soccer_dataset, batch_size=380)))['results']
    num_home_wins = 0
    num_draws = 0
    num_away_wins = 0
    for elem in PL_results:
        match elem:
            case 0:
                num_home_wins += 1
            case 1:
                num_draws += 1
            case 2:
                num_away_wins += 1
    print(num_home_wins)
    print(num_draws)
    print(num_away_wins)

    #Now test on the testing data
    other_league_dataset = SoccerDataset('../csv/PL_testing.csv', root_dir='/', transform=transform_to_float)
    dataloader = next(iter(DataLoader(other_league_dataset, batch_size=380)))
    outputs = torch.argmax(test_MLP(dataloader['stats']), dim=1)
    actual_results = dataloader['results'].reshape(380).long()
    correct = 0
    incorrect = 0
    for index, elem in enumerate(outputs):
        if elem == actual_results[index]:
            correct += 1
        else:
            incorrect += 1
    print(correct)
    print(incorrect)
    print(float(correct/(correct+incorrect)))
    


def tensor_to_float32(tensor):
    return tensor.astype(np.float32)
    

if __name__ == "__main__":
    main_function()