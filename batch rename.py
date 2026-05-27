import os
import shutil
import csv

# Set this to the folder where your numbered images AND names.csv are located
folder_path = "." 
os.chdir(folder_path)

# 1. Read the names from the CSV file
names = []
try:
    with open('names.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row: # Skip empty rows
                raw_name = row[0].strip()
                # Remove characters that aren't allowed in folder names
                safe_name = "".join(c for c in raw_name if c not in r'\/:*?"<>|')
                names.append(safe_name)
except FileNotFoundError:
    print("Error: Could not find names.csv. Make sure it's in the exact same folder!")
    exit()

# 2. Find and sort the image files numerically
files = [f for f in os.listdir('.') if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
files.sort(key=lambda x: int(os.path.splitext(x)[0]))

# 3. Group files into pairs, rename, and move them
for i in range(0, len(files), 2):
    if i + 1 < len(files):
        front_file = files[i]
        back_file = files[i+1]
        
        person_index = i // 2
        
        # Match the file pair to the name in the CSV
        if person_index < len(names):
            base_folder_name = names[person_index]
        else:
            base_folder_name = f"Unknown_Person_{person_index + 1}"
            
        # Handle duplicate names by adding _2, _3, etc.
        folder_name = base_folder_name
        counter = 2
        while os.path.exists(folder_name):
            folder_name = f"{base_folder_name}_{counter}"
            counter += 1
            
        os.makedirs(folder_name)
        
        # Grab the file extensions (e.g., '.png')
        front_ext = os.path.splitext(front_file)[1]
        back_ext = os.path.splitext(back_file)[1]
        
        # Move AND rename the files to "Front" and "Back"
        shutil.move(front_file, os.path.join(folder_name, f"Front{front_ext}"))
        shutil.move(back_file, os.path.join(folder_name, f"Back{back_ext}"))

print("Success! All IDs sorted into named folders and renamed to Front and Back.")