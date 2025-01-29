import random
import numpy as np
import torch
from collections import deque

class ReplayBuffer:
    
    def __init__(self, max_capacity: int, device: torch.device|str) -> None:
        """
        Replay Buffer memory to save the state, action, reward sequence from the current episode.
        
        Args:
            max_capacity (int): max buffer capacity.
            device (torch.device or int): device on which to save sampled transitions.
        """
        
        self.capacity = max_capacity
        self.device = device

        # deque for storing transitions
        self.buffer = deque(maxlen=self.capacity)


    def store(self, state, action, reward, next_state, done) -> None:
        """
        Store a transition into the buffer.
        
        Args:
            state (np.array): current state.
            action (int): action.
            reward (float): reward.
            next_state (np.array): next state.
            done (bool): terminal flag.
        """
        assert isinstance(state, np.ndarray), "Invalid state!"
        assert isinstance(action, int), "Invalid action!"
        assert isinstance(reward, float), "Invalid reward!"
        assert isinstance(next_state, np.ndarray), "Invalid next state!"
        assert isinstance(done, bool), "Invalid terminal flag!"

        self.buffer.append((state, action, reward, next_state, done))

    
    def sample(self, batch_size) -> tuple:
        """
        Sample a batch of transitions from the buffer.
        
        Args:
            batch_size (int): size of the batch.

        Returns:
            tuple: Batch of transitions.
        """

        assert self.size() >= batch_size, "Replay Buffer not big enough for sampling!"
        
        batch = random.sample(self.buffer, batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)
        
        return torch.tensor(np.array(states), dtype=torch.float32, device=self.device), \
            torch.tensor(actions, dtype=torch.float32, device=self.device).unsqueeze(-1), \
            torch.tensor(rewards, dtype=torch.float32, device=self.device).unsqueeze(-1), \
            torch.tensor(np.array(next_states), dtype=torch.float32, device=self.device), \
            torch.tensor(dones, dtype=torch.float32, device=self.device).unsqueeze(-1)

    def size(self) -> int:
        """
        Returns the current number of elements in the buffer.
        
        Returns:
            tuple: Batch of transitions.
        """
        
        return len(self.buffer)