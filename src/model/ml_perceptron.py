import torch.nn as nn

class Perceptron(nn.Module):
    

    def __init__(self, input_size, output_size):
        super(Perceptron, self).__init__()

        self.input_size = input_size

        self.lin1 = nn.Linear(input_size, output_size)

    def forward(self, x):
        
        out = self.lin1(x)

        return out