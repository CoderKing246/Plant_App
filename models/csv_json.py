import wikipedia
import json

plant_names = ['Orange', 'Corn_(maize)', 'Grape', 'Cherry_(including_sour)', 'Apple', 'Potato', 'Raspberry', 'Soybean', 'Pepper,_bell', 'Blueberry', 'Peach']

plant_info = {}

for plant in plant_names:
    try:
        summary = wikipedia.summary(plant + " plant", sentences=2)
        plant_info[plant] = {
            "scientific_name": wikipedia.page(plant + " plant").title,
            "description": summary
        }
    except:
        print(f"Could not find data for {plant}")

# Save to JSON
with open("plant_info.json", "w") as f:
    json.dump(plant_info, f, indent=4)

print("Plant details saved to plant_info.json")
