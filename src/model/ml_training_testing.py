from jobs.fetch_team_stats import DataFetcher
from jobs.create_csv import StoreCSV
from model.ml_perceptron import Perceptron
import os
from model.ml_dataset import SoccerDataset
import csv
import torch
from torch.utils.data import DataLoader
import torchvision
import numpy as np
import matplotlib.pyplot as plt

class TrainingTesting:
    
    def __init__(self) -> None:
        pass
    
    def training(self, train_data_loader, num_epochs, loss_function, optimizer, model):
        epochs = []
        losses = []
        for cur_epoch in range(num_epochs):
            cur_epoch_loss = 0.0
            for index, cur_batch in enumerate(train_data_loader):
                input_stats = cur_batch['stats']
                actual_results = cur_batch['results'].reshape(train_data_loader.batch_size).long()

                optimizer.zero_grad()

                outputs = model(input_stats)
                #Need to get outputs into a column tensor, can't have a row. len(outputs) is just the batch size
                loss = loss_function(outputs, actual_results)
                cur_epoch_loss += loss.item()
                loss.backward()

                optimizer.step()
            if cur_epoch % 10 == 0:
                epochs.append(cur_epoch)
                losses.append(cur_epoch_loss)
        #_plot_accuracy_history(epochs, losses)
        # print(losses[0])
        # print(losses[-1])

    def testing(self, testing_dataloader, loss_function, model):
        for index, cur_batch in enumerate(testing_dataloader):
            input_stats = cur_batch['stats']
            output_scores = cur_batch['scores']

            outputs = model(input_stats)
            loss = loss_function(outputs, output_scores)
            print(loss.item())

def _plot_accuracy_history(x_data, y_data):
    plt.figure()	
    plt.plot(x_data, y_data)
    plt.legend()
    plt.savefig("plot_cost_history.png")