from typing import OrderedDict
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.models as models


class ChannelAttention(nn.Module):
    def __init__(self, in_channels, reduction_ratio=16):
        super(ChannelAttention, self).__init__()
        self.avg_pool = nn.AdaptiveAvgPool2d(1)
        self.max_pool = nn.AdaptiveMaxPool2d(1)
        self.fc1 = nn.Conv2d(in_channels, in_channels // reduction_ratio, kernel_size=1)
        self.relu = nn.ReLU()
        self.fc2 = nn.Conv2d(in_channels // reduction_ratio, in_channels, kernel_size=1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        avg_pool = self.avg_pool(x)
        max_pool = self.max_pool(x)
        avg_out = self.fc2(self.relu(self.fc1(avg_pool)))
        max_out = self.fc2(self.relu(self.fc1(max_pool)))
        attention = self.sigmoid(avg_out + max_out)
        return x * attention


class SpatialAttention(nn.Module):
    def __init__(self, kernel_size=7):
        super(SpatialAttention, self).__init__()
        self.conv = nn.Conv2d(2, 1, kernel_size=kernel_size, padding=(kernel_size - 1) // 2)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        avg_pool = torch.mean(x, dim=1, keepdim=True)
        max_pool, _ = torch.max(x, dim=1, keepdim=True)
        pool = torch.cat([avg_pool, max_pool], dim=1)
        attention = self.sigmoid(self.conv(pool))
        return x * attention


class CBAM(nn.Module):
    def __init__(self, in_channels, reduction_ratio=8, spatial_kernel_size=7):
        super(CBAM, self).__init__()
        self.channel_attention = ChannelAttention(in_channels, reduction_ratio)
        self.spatial_attention = SpatialAttention(spatial_kernel_size)

    def forward(self, x):
        x = self.channel_attention(x)
        x = self.spatial_attention(x)
        return x


class SiameseResNet(nn.Module):
    def __init__(self, model_name='resnet18', pretrained=False):
        super(SiameseResNet, self).__init__()
        self.baseModel = models.resnet18(pretrained=pretrained)

        self.attention1 = CBAM(in_channels=64)  # CBAM for layer 1
        self.attention2 = CBAM(in_channels=256)  # CBAM for layer 3

        self.baseModel.conv1 = nn.Conv2d(1, 64, kernel_size=7, stride=2, padding=3, bias=False)
        self.baseModel.fc = nn.Identity()  # Remove the fully connected layer

    def forward(self, x):
        out = self.baseModel.conv1(x)
        out = self.baseModel.bn1(out)
        out = self.baseModel.relu(out)
        out = self.baseModel.maxpool(out)

        out = self.attention1(self.baseModel.layer1(out))  # Applying CBAM to layer 1
        out = self.baseModel.layer2(out)
        out = self.attention2(self.baseModel.layer3(out))  # Applying CBAM to layer 3
        out = self.baseModel.layer4(out)

        out = F.adaptive_avg_pool2d(out, (1, 1))  # Global Average Pooling
        out = torch.flatten(out, 1)
        return out


class LogisticSiameseRegression(nn.Module):
    def __init__(self, model):
        super(LogisticSiameseRegression, self).__init__()

        self.model = model
        self.fc = nn.Sequential(
            nn.Linear(512, 256),
            nn.LeakyReLU(inplace=True),
            nn.Dropout(0.2),
            nn.Linear(256, 128),
            nn.LeakyReLU(inplace=True),
            nn.Linear(128, 1),
        )
        self.sigmoid = nn.Sigmoid()

    def forward_once(self, x):
        out = self.model(x)
        out = F.normalize(out, p=2, dim=1)
        return out

    def forward(self, x1, x2):
        out1 = self.forward_once(x1)
        out2 = self.forward_once(x2)

        diff = out1 - out2
        out = self.fc(diff)
        out = self.sigmoid(out)
        return out


class TriangularMarginLoss(nn.Module):
    def __init__(self, margin=0.5):
        super(TriangularMarginLoss, self).__init__()
        self.margin = margin

    def forward(self, anchor, positive, negative):
        distance_anchor_positive = F.pairwise_distance(anchor, positive, p=2)
        distance_anchor_negative = F.pairwise_distance(anchor, negative, p=2)

        loss = torch.relu(distance_anchor_positive - distance_anchor_negative + self.margin)

        return loss.mean()
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

import json
import os
import ipfshttpclient
import torch
from web3 import Web3

# Connect to IPFS
client = ipfshttpclient.connect("/ip4/127.0.0.1/tcp/5001")  # Ensure IPFS daemon is running

# Connect to Blockchain
web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))  # Ganache RPC URL
contract_address = "0x5b4862896e6a36030a721446AC10e5a0F03205B3"
account = "0xf5a9C47edC1e713BBD4e97b23486841663e8D9EC"  # Ethereum account

# Load Smart Contract ABI
with open("C:/Users/HP/Desktop/blockchainCheque/build/contracts/ModelCIDStorage.json") as f:
    contract_abi = json.load(f)["abi"]

contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Retrieve CID from Blockchain
model_cid = contract.functions.getCID(account).call()
print(f"🔍 Retrieved Model CID from Blockchain: {model_cid}")

# Check if CID is valid
if not model_cid or not isinstance(model_cid, str):
    raise ValueError("❌ Invalid model CID retrieved from blockchain.")

# Define model save path
model_path = "./logistic_siamese_model.pth"

# Download model file directly from IPFS
try:
    model_data = client.cat(model_cid)  # Fetch entire file directly
    with open(model_path, "wb") as f:
        f.write(model_data)
    print(f"✅ Model successfully downloaded and saved as: {model_path}")

    # Verify Model Integrity
    try:
        model = torch.load(model_path, map_location=torch.device("cpu"))
        print("✅ Model loaded successfully!")
    except Exception as e:
        print(f"❌ Model loading failed: {e}")

except Exception as e:
    print(f"❌ Error downloading model from IPFS: {e}")


# Initialize Siamese Model
siamese_model = SiameseResNet(pretrained=True).to(device)
model = LogisticSiameseRegression(siamese_model).to(device)

# Load the state dict
state_dict = torch.load(model_path, map_location=device)

# Remove "module." prefix if it exists
new_state_dict = OrderedDict()
for k, v in state_dict.items():
    new_key = k.replace("module.", "")
    new_state_dict[new_key] = v

filtered_state_dict = {k: v for k, v in new_state_dict.items() if k in model.state_dict()}

# Load the filtered state dict
model.load_state_dict(filtered_state_dict, strict=False)
model.eval()