import json
import torch
import numpy as np
import pandas as pd
from torch.utils.data import Dataset, DataLoader, random_split, Subset, TensorDataset, default_collate

class SoccerDataset(Dataset):
    

    def __init__(self, csv_file, root_dir, transform=None):
        
        temp_frame = pd.read_csv(csv_file)
        results = []
        for index, row in temp_frame.iterrows():
            #Home win
            if row['Home Outcome Score'] > row['Away Outcome Score']:
                results.append(0)
            #Draw
            elif row['Home Outcome Score'] == row['Away Outcome Score']:
                results.append(1)
            #Away win
            else:
                results.append(2)
        temp_frame = temp_frame.drop(columns=['Home Outcome Score', 'Away Outcome Score'])
        temp_frame.insert(len(temp_frame.columns), "Result", results)

        self.soccer_data_frame = temp_frame
        
        #This for now isn't needed because inputs and their labels are in the same csv files
        self.root_dir = root_dir
        self.transform = transform

    def __len__(self):
        return len(self.soccer_data_frame)
    
    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()

        rows = self.soccer_data_frame.iloc[idx, :]
        split_idx = len(rows) - 1
        stats = rows[:split_idx]
        results = rows[split_idx:]
        stats = np.array(stats)
        results = np.array(results)
        
        sample = {'stats': stats, 'results': np.asarray(results)}

        if self.transform:
            sample = {'stats': self.transform(sample['stats']), 'results': self.transform(sample['results'])}

        return sample
