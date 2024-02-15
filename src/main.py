from jobs.fetch_team_stats import DataFetcher
from jobs.create_csv import StoreCSV
from model.ml_perceptron import Perceptron
from model.ml_mlp import MultiLayerPerceptron
import os
from model.ml_dataset import SoccerDataset
from model.ml_training_testing import TrainingTesting
import csv
import torch
from torch.utils.data import DataLoader, Subset
import torchvision
import numpy as np
import tensorflow as tf
from sklearn.model_selection import KFold


def main_function():
    

    leagues = ['PL', 'SerieA', 'Bundesliga', 'Ligue1', 'LaLiga']
    test_obj = StoreCSV()
    #This is code 
    #for league in leagues:
    #    test_obj.createCSV(league)
    #os.rename(f'{league}.csv', f'../csv/{league}.csv')
    transform_to_float = tensor_to_float32
    soccer_dataset = SoccerDataset('../csv/PL.csv', root_dir='/', transform=transform_to_float)

    #this should be [1^-10, 10^-9,...,0.1]
    possible_learning_rates = [10**i for i in list(range(-6,-1))]
    #this should be [0, 0.01, ..., 0.1]
    possible_reg_params = [0.01*i for i in list(range(0,10))]
    possible_batch_sizes = [4, 19, 38, 76]
    best_training_accuracy = 0
    best_lr = None
    best_reg_param = None
    best_batch_size = None
    #For multiclass classification
    loss_fn = torch.nn.CrossEntropyLoss()

    kFold=KFold(n_splits=5,shuffle=True)
    indices = list(range(380))
    for cur_lr in possible_learning_rates:
        for cur_reg_param in possible_reg_params:
            for cur_batch_size in possible_batch_sizes:
                total_acc = 0
                for train_index,test_index in kFold.split(indices):
                    sub_soccer_dataset = Subset(soccer_dataset, train_index)
                
                    dataloader = DataLoader(sub_soccer_dataset, batch_size=cur_batch_size)
                    #3 possible output values so output size of MLP is 3:
                    test_MLP = MultiLayerPerceptron(108, 3)
                    optimizer = torch.optim.Adam(test_MLP.parameters(), lr=cur_lr, weight_decay=cur_reg_param)
                    training_obj = TrainingTesting()
                    #was 1000
                    training_obj.training(dataloader, 100, loss_fn, optimizer, test_MLP)

                    validation_dataloader = iter(DataLoader(Subset(soccer_dataset, test_index), batch_size=76))

                    validation_data = next(validation_dataloader)
                    outputs = torch.argmax(test_MLP(validation_data['stats']), dim=1)
                    actual_results = validation_data['results'].reshape(76).long()
                    correct = 0
                    incorrect = 0
                    for index, elem in enumerate(outputs):
                        if elem == actual_results[index]:
                            correct += 1
                        else:
                            incorrect += 1
                    total_acc += float(correct/(correct+incorrect))
                print(cur_lr)
                print(cur_reg_param)
                print(cur_batch_size)
                print(float(total_acc/5))
                if float(total_acc/5) > best_training_accuracy:
                    best_training_accuracy = float(total_acc/5)
                    best_lr = cur_lr
                    best_reg_param = cur_reg_param
                    best_batch_size = cur_batch_size

    dataloader = DataLoader(soccer_dataset, batch_size=best_batch_size)
    final_MLP = MultiLayerPerceptron(108, 3)
    optimizer = torch.optim.Adam(final_MLP.parameters(), lr=best_lr, weight_decay=best_reg_param)
    training_obj = TrainingTesting()
    training_obj.training(dataloader, 1000, loss_fn, optimizer, final_MLP)

    #Now test on the testing data
    testing_dataset = SoccerDataset('../csv/PL_testing.csv', root_dir='/', transform=transform_to_float)
    testing_dataloader = next(iter(DataLoader(testing_dataset, batch_size=380)))

    outputs = torch.argmax(final_MLP(testing_dataloader['stats']), dim=1)
    actual_results = testing_dataloader['results'].reshape(380).long()
    correct = 0
    incorrect = 0
    for index, elem in enumerate(outputs):
        if elem == actual_results[index]:
            correct += 1
        else:
            incorrect += 1
    print(best_lr)
    print(best_reg_param)
    print(best_batch_size)
    print(best_training_accuracy)
    print(float(correct/(correct+incorrect)))

def tensor_to_float32(tensor):
    return tensor.astype(np.float32)
    

if __name__ == "__main__":
    main_function()


#    PL_results =  next(iter(DataLoader(soccer_dataset, batch_size=380)))['results']
#     # num_home_wins = 0
#     # num_draws = 0
#     # num_away_wins = 0
#     # for elem in PL_results:
#     #     match elem:
#     #         case 0:
#     #             num_home_wins += 1
#     #         case 1:
#     #             num_draws += 1
#     #         case 2:
#     #             num_away_wins += 1
#     # print(num_home_wins)
#     # print(num_draws)
#     # print(num_away_wins)