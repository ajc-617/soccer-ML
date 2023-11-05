import torch.nn as nn

class MultiLayerPerceptron(nn.Module):
    

    def __init__(self, input_size, output_size):
        

        super(MultiLayerPerceptron, self).__init__()

        self.relu = nn.ReLU()
        #this will be 108
        self.input_size = input_size
        #output size will be 4
        self.lin1 = nn.Linear(input_size, 50)
        self.lin2 = nn.Linear(50, 15)
        self.lin3 = nn.Linear(15, output_size)


    def forward(self, x):
        
        #input matrix is 380x108
        out = self.lin1(x)
        out - self.relu(out)
        out = self.lin2(out)
        out = self.relu(out)
        out = self.lin3(out)

        #output is 380x2 if batch size is 380 (one season)
        return out