"""
PyTorch Models for Trading Strategy Prediction and RL Training
"""

import torch
import torch.nn as nn
import torch.optim as optim
from typing import Tuple


class TradingNN(nn.Module):
    """
    Neural Network for trade prediction
    
    Input: 64 features (prices, volumes, indicators)
    Output: 3 signals (0=hold, 1=buy, 2=sell)
    """
    
    def __init__(self, input_size: int = 64, hidden_size: int = 128):
        super(TradingNN, self).__init__()
        
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu1 = nn.ReLU()
        self.dropout1 = nn.Dropout(0.3)
        
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.relu2 = nn.ReLU()
        self.dropout2 = nn.Dropout(0.3)
        
        self.fc3 = nn.Linear(hidden_size, 64)
        self.relu3 = nn.ReLU()
        
        self.fc4 = nn.Linear(64, 3)  # 3 actions: hold, buy, sell
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass"""
        x = self.fc1(x)
        x = self.relu1(x)
        x = self.dropout1(x)
        
        x = self.fc2(x)
        x = self.relu2(x)
        x = self.dropout2(x)
        
        x = self.fc3(x)
        x = self.relu3(x)
        
        x = self.fc4(x)
        return x


class LSTMTrader(nn.Module):
    """
    LSTM-based model for sequential price prediction
    
    Captures temporal patterns in market data
    """
    
    def __init__(self, input_size: int = 5, hidden_size: int = 64, num_layers: int = 2):
        super(LSTMTrader, self).__init__()
        
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True, dropout=0.3)
        self.fc1 = nn.Linear(hidden_size, 32)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(32, 3)  # 3 actions
        
    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, Tuple]:
        """
        Forward pass
        
        Args:
            x: Input tensor of shape (batch_size, sequence_length, input_size)
            
        Returns:
            Predictions of shape (batch_size, 3) and LSTM hidden states
        """
        lstm_out, hidden = self.lstm(x)
        last_out = lstm_out[:, -1, :]  # Take last time step
        
        x = self.fc1(last_out)
        x = self.relu(x)
        x = self.fc2(x)
        
        return x, hidden


class DualNetworkTrader(nn.Module):
    """
    Dual network architecture combining CNN for feature extraction 
    and LSTM for temporal analysis
    """
    
    def __init__(self):
        super(DualNetworkTrader, self).__init__()
        
        # CNN for feature extraction
        self.conv1 = nn.Conv1d(5, 32, kernel_size=5, padding=2)
        self.relu1 = nn.ReLU()
        self.pool1 = nn.MaxPool1d(2)
        
        self.conv2 = nn.Conv1d(32, 64, kernel_size=3, padding=1)
        self.relu2 = nn.ReLU()
        self.pool2 = nn.MaxPool1d(2)
        
        # LSTM for temporal patterns
        self.lstm = nn.LSTM(64, 128, num_layers=2, batch_first=True, dropout=0.3)
        
        # Dense layers for decision making
        self.fc1 = nn.Linear(128, 64)
        self.relu3 = nn.ReLU()
        self.dropout = nn.Dropout(0.3)
        self.fc2 = nn.Linear(64, 3)  # 3 actions
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass combining CNN and LSTM
        
        Args:
            x: Input tensor of shape (batch_size, sequence_length, 5_features)
            
        Returns:
            Action predictions of shape (batch_size, 3)
        """
        # CNN feature extraction
        x = x.transpose(1, 2)  # (batch, 5, seq_len)
        x = self.conv1(x)
        x = self.relu1(x)
        x = self.pool1(x)
        
        x = self.conv2(x)
        x = self.relu2(x)
        x = self.pool2(x)
        
        x = x.transpose(1, 2)  # Back to (batch, seq_len, features)
        
        # LSTM temporal analysis
        lstm_out, _ = self.lstm(x)
        x = lstm_out[:, -1, :]  # Take last time step
        
        # Decision layers
        x = self.fc1(x)
        x = self.relu3(x)
        x = self.dropout(x)
        x = self.fc2(x)
        
        return x


class DistilledStudentModel(nn.Module):
    """
    Smaller, faster student model for edge deployment
    Trained via knowledge distillation from larger teacher models
    """
    
    def __init__(self, input_size: int = 64, hidden_size: int = 32):
        super(DistilledStudentModel, self).__init__()
        
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, 16)
        self.relu2 = nn.ReLU()
        self.fc3 = nn.Linear(16, 3)
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass - minimal computation for real-time inference"""
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        x = self.relu2(x)
        x = self.fc3(x)
        return x


def knowledge_distillation_loss(
    student_output: torch.Tensor,
    teacher_output: torch.Tensor,
    target: torch.Tensor,
    temperature: float = 4.0,
    alpha: float = 0.7
) -> torch.Tensor:
    """
    Knowledge distillation loss combining:
    - KL divergence from teacher (soft targets)
    - Cross-entropy with true labels (hard targets)
    
    Args:
        student_output: Logits from student model
        teacher_output: Logits from teacher model
        target: True labels
        temperature: Temperature for softening probabilities
        alpha: Weight between KL divergence and cross-entropy
        
    Returns:
        Combined loss value
    """
    # KL divergence loss (learn from teacher)
    kl_loss = nn.KLDivLoss(reduction='batchmean')(
        nn.LogSoftmax(dim=1)(student_output / temperature),
        nn.Softmax(dim=1)(teacher_output / temperature)
    )
    
    # Cross-entropy loss (learn ground truth)
    ce_loss = nn.CrossEntropyLoss()(student_output, target)
    
    # Combined loss
    loss = alpha * kl_loss + (1 - alpha) * ce_loss
    
    return loss


# Example usage for model creation and export
if __name__ == "__main__":
    # Create models
    trader_nn = TradingNN()
    lstm_trader = LSTMTrader()
    dual_network = DualNetworkTrader()
    student_model = DistilledStudentModel()
    
    # Example: Save models
    torch.save(trader_nn.state_dict(), "trader_nn.pt")
    torch.save(lstm_trader.state_dict(), "lstm_trader.pt")
    torch.save(dual_network.state_dict(), "dual_network.pt")
    torch.save(student_model.state_dict(), "student_model.pt")
    
    print("Models created and saved successfully!")
