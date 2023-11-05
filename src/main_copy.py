from jobs.fetch_team_stats import DataFetcher
from jobs.create_csv import StoreCSV
from model.ml_perceptron import Perceptron
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
    #for league in leagues:
    #    test_obj.createCSV(league)
    #os.rename(f'{league}.csv', f'../csv/{league}.csv')
    transform_to_float = tensor_to_float32
    soccer_dataset = SoccerDataset('../csv/PL.csv', root_dir='/', transform=transform_to_float)
    sample = soccer_dataset[0]
    print(sample['stats'].shape)
    print(sample['scores'].shape)

    dataloader = DataLoader(soccer_dataset, batch_size=32)
    test_perceptron = Perceptron(108, 2)
    #sample_input = test_perceptron(next(iter(dataloader))['stats'])
    loss_fn = torch.nn.MSELoss()
    #dummy_losses = torch.ones((32,4))
    #print(loss_fn(sample_input,dummy_losses))
    optimizer = torch.optim.Adam(test_perceptron.parameters(), lr=0.00001)
    training_obj = TrainingTesting()
    training_obj.training(dataloader, 1000, loss_fn, optimizer, test_perceptron)

    testing_dataset = SoccerDataset('../csv/PL.csv', root_dir='/', transform=transform_to_float)
    #dataloader = DataLoader(testing_dataset, batch_size=32)
    #training_obj.testing(dataloader, loss_fn, test_perceptron)
    leagues[0] = 'PL_testing'
    leagues.append('PL')
    for league in leagues:
        num_correct = 0
        num_non_draws = 0
        testing_dataset = SoccerDataset(f'../csv/{league}.csv', root_dir='/', transform=transform_to_float)
        for index in range(len(testing_dataset)):
            out = test_perceptron(torch.from_numpy(testing_dataset[index]['stats']))
            actual = torch.from_numpy(testing_dataset[index]['scores'])
            #Don't care about draws for now
            if (actual[0].item() == actual[1].item()):
                continue
            num_non_draws += 1
            #Model correctly guessed home win
            if (actual[0].item() > actual[1].item() and out[0].item() > out[1].item()):
                num_correct += 1
            if (actual[0].item() < actual[1].item() and out[0].item() < out[1].item()):
                num_correct += 1
        print(float(num_correct/num_non_draws))
    for league in leagues:
        num_correct = 0
        num_draws = 0
        testing_dataset = SoccerDataset(f'../csv/{league}.csv', root_dir='/', transform=transform_to_float)
        for index in range(len(testing_dataset)):
            out = test_perceptron(torch.from_numpy(testing_dataset[index]['stats']))
            actual = torch.from_numpy(testing_dataset[index]['scores'])
            #Don't care about wins on either side only draws
            if not actual[0].item() == actual[1].item():
                continue
            num_draws += 1
            if round(out[0].item()) == round(out[1].item()):
                num_correct += 1

        #print(float(num_correct/num_draws))
        #print(num_draws)
        
        #print("predicted:")
        #print(out)
        #print("actual:")
        #print(actual)
    
    


def tensor_to_float32(tensor):
    return tensor.astype(np.float32)
    

if __name__ == "__main__":
    main_function()