import os
import pandas as pd
import json

# Get the folder where this script file lives
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Construct the full path to CSV
csv_path = os.path.join(BASE_DIR, "survey_results_public.csv")

df = pd.read_csv(csv_path)


skill_columns = [
    "LanguageHaveWorkedWith",
    "DatabaseHaveWorkedWith",
    "PlatformHaveWorkedWith",
    "WebframeHaveWorkedWith",
    "MiscTechHaveWorkedWith",
    "ToolsTechHaveWorkedWith",
]


existing_columns = [col for col in skill_columns if col in df.columns]
print(existing_columns)

skills_set = set()

for col in existing_columns:
    for entry in df[col].dropna():
        for skill in entry.split(';'):
            skills_set.add(skill.strip())

skills_list = sorted(skills_set)
print(skills_list[:20])


with open("skills_list.json", "w") as f:
    json.dump(skills_list, f)
print("Skills list saved to skills_list.json")