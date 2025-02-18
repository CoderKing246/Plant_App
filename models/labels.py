import os

# Path to dataset folder
dataset_path = "datasets/"

# Get all folder names (these are the class labels)
labels = sorted(os.listdir(dataset_path))

# Write labels to a file
with open("labels.txt", "w") as f:
    for label in labels:
        f.write(label + "\n")

print("✅ labels.txt created successfully!")
