import numpy as np

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

from torch.distributions import Categorical

class ReinforceAgent:
    """
    A wrapper around a PyTorch reinforce model for Kalah
    """

    def __init__(self, policy, seed=543):
        self.policy = policy

    def _get_obs(self, board):
        player_board_one = board._get_player_board(0)[:-1]
        player_board_two = board._get_player_board(1)[:-1]

        board_obs = player_board_one + player_board_two
        obs = np.array(board_obs)/(2*board.bins)
        return obs

    def select_action(self, state):
        state = torch.from_numpy(state).float().unsqueeze(0)
        probs = self.policy(state)
        m = Categorical(probs)

        return m.sample().item()

    def get_next_move(self, board):
        obs = self._get_obs(board)
        return self.select_action(obs)
