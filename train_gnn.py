import torch
from gnn_model import WalletGNN

def train(model, data, epochs=200):
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

    for epoch in range(epochs):
        optimizer.zero_grad()
        out = model(data)

        # fake labels: high degree = suspicious (hackathon trick)
        labels = (data.x[:,0] + data.x[:,1] > 4).float().unsqueeze(1)

        loss = torch.nn.functional.mse_loss(out, labels)
        loss.backward()
        optimizer.step()

    return out.detach()
