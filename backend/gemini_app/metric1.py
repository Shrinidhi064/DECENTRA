import matplotlib.pyplot as plt
import numpy as np

# Data
models = [
    "Logistic Siamese Regression",
    "Logistic Siamese Regression\n(ResNet34 + CBAM)",
    "Logistic Siamese Regression\n(ResNet50 + CBAM)",
    "Siamese + SVM",
    "Siamese + SVM (RBF, Balanced)",
    "Siamese + SVM (C=100)",
    "Siamese + RandomForest",
    "Siamese + XGBoost",
    "Siamese + LightGBM",
    "Siamese + KNN",
    "Siamese + Naive Bayes",
    "Siamese + Decision Tree",
    "Siamese + MLP",
    "Siamese + MLP (Tuned)"
]

accuracy = [81, 79.92, 76, 59, 63, 64, 57, 64.25, 64.33, 60, 60, 57.43, 64.89, 65.10]

# Plot
fig, ax = plt.subplots(figsize=(12, 6))
y_pos = np.arange(len(models))
bars = ax.barh(y_pos, accuracy, color='skyblue', edgecolor='black')

# Add data labels
for bar in bars:
    plt.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
             f'{bar.get_width():.2f}%', va='center', fontsize=10)

# Formatting
ax.set_yticks(y_pos)
ax.set_yticklabels(models, fontsize=10)
ax.set_xlabel("Accuracy (%)", fontsize=12)
ax.set_title("Accuracy Comparison of Siamese-Based Models", fontsize=14, fontweight='bold')
ax.invert_yaxis()  # Invert for better readability

plt.grid(axis='x', linestyle='--', alpha=0.6)
plt.show()
