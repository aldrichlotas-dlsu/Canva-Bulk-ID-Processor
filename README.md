# PVC ID Automator 🪪

A lightweight set of Python scripts designed to completely automate the post-processing of bulk-generated PVC IDs (like those exported from Canva's Bulk Create tool). 

Instead of manually renaming hundreds of files and painstakingly cropping out ID punch holes one by one, this tool sorts your files into individual folders based on a spreadsheet and acts as an automated cookie-cutter to punch perfectly uniform, transparent holes into every ID.

## ✨ Features
* **Batch Sorting:** Reads a `names.csv` file and automatically pairs sequential `1.png` and `2.png` files into folders named after each person.
* **Smart Renaming:** Renames numbered files into clean `Front.png` and `Back.png` formats.
* **Duplicate Handling:** Automatically appends numbers (e.g., `John Doe_2`) if multiple people share the same name on the spreadsheet.
* **Automated Hole Punching:** Uses a master `mask.png` template to delete specific pixels across all ID files, leaving a clean, transparent hole for physical lanyard punching.
* **One-Click Execution:** Runs entirely via a `.bat` file within an isolated Python virtual environment to prevent system conflicts.

## 📁 Required Folder Structure
Before running the tool, your root directory must look exactly like this:

```text
/pvc-id-automator
│
├── 1.png             # Extracted Canva export (Front)
├── 2.png             # Extracted Canva export (Back)
├── 3.png             # Extracted Canva export (Front)
├── 4.png             # Extracted Canva export (Back)
│
├── names.csv         # A single-column CSV of names in chronological order (No header row!)
├── mask.png          # Template image (same dimensions as IDs) with a solid colored hole
│
├── batch rename.py   # Script 1: Sorter and Renamer
├── mask.py           # Script 2: Hole Puncher
└── auto_run.bat      # The master execution file