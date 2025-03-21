import torch
import torch.nn as nn
import torch.nn.functional as F


class DQN(nn.Module):
    def __init__(self, state_dim, hidden_layers, action_dim):
        """
        Initialize parameters and build model.
        
        Parameters
        ----------
            state_dim: int
                Dimension of each state.
            hidden_layers: list
                List of number of hidden nodes.
            action_dim: int
                Dimension of action space.
        """
        super(DQN, self).__init__()
        assert len(hidden_layers)>0, "Invalid input! There must be at least one hidden layer."
        
        # model attributes
        self.input_dim = state_dim
        self.output_dim = action_dim
        # network
        prev_size = self.input_dim
        self.linears = nn.ModuleList()
        for l_size in hidden_layers:
            self.linears.append(nn.Linear(prev_size, l_size))
            prev_size = l_size
        self.linear_out = nn.Linear(prev_size, self.output_dim)

        
    def forward(self, x):
        """
        Map state -> action values.

        Parameters
        ----------
            x: torch.Tensor
                Input tensor.
        """
        for l in self.linears:
            x = F.relu(l(x))
            #print(x)
            #assert not torch.isnan(x).any(), "NaN detected!"
        out = self.linear_out(x)
        
        return out