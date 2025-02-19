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
    storeCSV = StoreCSV()
    storeCSV.createAllCSV()
    

if __name__ == "__main__":
    main_function()

#test