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
    
    #Need to convert input data to float 32
    transform_to_float = tensor_to_float32
    soccer_dataset = SoccerDataset('../csv/PL.csv', root_dir='/', transform=transform_to_float)

    #possible learnong rates of [1^-4, 1^-3,...,0.1]
    possible_learning_rates = [10**i for i in list(range(-4,-1))]
    #possible regularization parameters of [0.01, ..., -0.1]
    possible_reg_params = [0.01*i for i in list(range(0,10))]
    #possible batch sizes of [5, ..., 45]
    possible_batch_sizes = list(range(5, 50, 5))
    #Initialze best training accuracy to 0 so after the first run, as long as hyperparams don't yield 0 accuracy, they will no longer be None
    best_training_accuracy = 0
    #Keep track of best learning rate, regularization parameter, and batch size that yieldbest result
    best_lr = None
    best_reg_param = None
    best_batch_size = None
    #For multiclass classification, best to use cross entropy loss
    loss_fn = torch.nn.CrossEntropyLoss()

    #Set up kfold cross validation with 5 splits
    kFold=KFold(n_splits=5,shuffle=True)
    indices = list(range(380))
    #get the number of splits used into a variable for later
    num_splits = kFold.get_n_splits(indices)
    #loop through every possible learning rate, regularization parameter, batch size commbination to see whichone yields best validation accuracy
    for cur_lr in possible_learning_rates:
        for cur_reg_param in possible_reg_params:
            for cur_batch_size in possible_batch_sizes:
                #Need to keep track of total accuracy for 5 runs of k fold, then average total accuracy to see if its better than best_training_accuracy
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

                    validation_dataloader = iter(DataLoader(Subset(soccer_dataset, test_index), batch_size=int(380/num_splits)))

                    validation_data = next(validation_dataloader)
                    outputs = torch.argmax(test_MLP(validation_data['stats']), dim=1)
                    actual_results = validation_data['results'].reshape(int(380/num_splits)).long()
                    correct = 0
                    incorrect = 0
                    for index, elem in enumerate(outputs):
                        if elem == actual_results[index]:
                            correct += 1
                        else:
                            incorrect += 1
                    total_acc += float(correct/(correct+incorrect))
                print(f"current learning rate: {cur_lr}")
                print(f"current regularization: {cur_reg_param}")
                print(f"current batch size: {cur_batch_size}")
                print(f"accuracy: {float(total_acc/num_splits)}")
                if float(total_acc/num_splits) > best_training_accuracy:
                    best_training_accuracy = float(total_acc/num_splits)
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
    print(f"best learning rate: {best_lr}")
    print(f"best regularization parameter: {best_reg_param}")
    print(f"best batch size: {best_batch_size}")
    print(f"best training accuracy: {best_training_accuracy}")
    print(f"testing accuracy: {float(correct/(correct+incorrect))}")

def tensor_to_float32(tensor):
    return tensor.astype(np.float32)
    
if __name__ == "__main__":
    main_function()