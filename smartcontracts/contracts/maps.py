import torch
import matplotlib.pyplot as plt

# Suppose this is the output of ResNet18 for a signature
# shape: [512, 7, 7]
features = torch.rand(512, 7, 7)

# Choose a few feature maps to view
selected_channels = [0, 50, 120, 300, 511]

plt.figure(figsize=(12, 3))
for i, idx in enumerate(selected_channels):
    plt.subplot(1, 5, i + 1)
    plt.imshow(features[idx], cmap='viridis')
    plt.title(f'Channel {idx}')
    plt.axis('off')

plt.suptitle("Visualizing 7x7 Feature Maps from ResNet18")
plt.show()
