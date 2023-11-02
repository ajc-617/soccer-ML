import json
import torch
import numpy as np
import pandas as pd
from torch.utils.data import Dataset, DataLoader, random_split, Subset, TensorDataset, default_collate

class SoccerDataset(Dataset):
    
    def __init__(self, csv_file, root_dir, transform=None):
        super().__init__()