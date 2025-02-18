import os

# Path to PlantVillage dataset
dataset_path = "datasets/"

# Extract unique plant names
plant_names = set()
for folder in os.listdir(dataset_path):
    if "___" in folder:  # Ignore disease names
        plant_name = folder.split("___")[0]
        plant_names.add(plant_name)

# Print unique plant names
print(plant_names)
