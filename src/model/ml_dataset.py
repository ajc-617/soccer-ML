import json
import torch
import numpy as np
import pandas as pd
from torch.utils.data import Dataset, DataLoader, random_split, Subset, TensorDataset, default_collate

class SoccerDataset(Dataset):
    

    def __init__(self, csv_file, root_dir, transform=None):
        
        self.soccer_data_frame = pd.read_csv(csv_file)
        #This for now isn't needed because inputs and their labels are in the same csv files
        self.root_dir = root_dir
        self.transform = transform

    def __len__(self):
        return len(self.soccer_data_frame)
    
    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()

        rows = self.soccer_data_frame.iloc[idx, :]
        split_idx = len(rows) - 4
        stats = rows[:split_idx]
        scores = rows[split_idx:]
        stats = np.array(stats)
        scores = np.array(scores)

        sample = {'stats': stats, 'scores': scores}

        if self.transform:
            sample = self.transform(sample)

        return sample
