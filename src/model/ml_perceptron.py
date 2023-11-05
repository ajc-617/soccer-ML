import torch.nn as nn

class Perceptron(nn.Module):
    

    def __init__(self, input_size, output_size):
        

        super(Perceptron, self).__init__()

        #this will be 108
        self.input_size = input_size
        #output size will be 4
        self.lin1 = nn.Linear(input_size, output_size)

    def forward(self, x):
        
        #input matrix is 380x108
        out = self.lin1(x)

        return out