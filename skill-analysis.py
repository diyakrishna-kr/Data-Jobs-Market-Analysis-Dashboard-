# Stage 3: Skill Analysis

import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import ast

# Load cleaned dataset
df = pd.read_csv("data_jobs_cleaned2.csv")


# --------------------------------------------------
# Convert skills_extracted back into Python lists
# --------------------------------------------------

def convert_to_list(value):
    if pd.isna(value):
        return []
    
    if isinstance(value, list):
        return value
    
    try:
        return ast.literal_eval(value)
    except:
        return []


df["skills_extracted"] = df["skills_extracted"].apply(convert_to_list)


# --------------------------------------------------
# 1. Top 10 Most Demanded Skills
# --------------------------------------------------

all_skills = [
    skill.strip()
    for skills in df["skills_extracted"]
    for skill in skills
    if isinstance(skill, str) and skill.strip()
]

skill_counts = Counter(all_skills)

top_skills = skill_counts.most_common(10)

print(" Top 10 Skills in Demand:")
for skill, count in top_skills:
    print(f"{skill}: {count}")


# --------------------------------------------------
# Visualization: Top 10 Skills
# --------------------------------------------------

skills = [item[0] for item in top_skills]
counts = [item[1] for item in top_skills]

plt.figure(figsize=(12, 6))

bars = plt.bar(skills, counts)

plt.title("Top 10 Skills in Demand")
plt.xlabel("Skill")
plt.ylabel("Number of Job Postings")

# Make skill names readable
plt.xticks(rotation=45, ha="right")

# Add values above bars
for bar, count in zip(bars, counts):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),
        f"{count:,}",
        ha="center",
        va="bottom"
    )

plt.tight_layout()
plt.show()


# --------------------------------------------------
# 2. Skills by Job Role
# --------------------------------------------------

selected_role = "Machine Learning Engineer"

ml_skills = df[
    df["job_title"].str.strip().str.lower() == selected_role.lower()
]["skills_extracted"]

ml_skill_counts = Counter(
    skill.strip()
    for skills in ml_skills
    for skill in skills
    if isinstance(skill, str) and skill.strip()
).most_common(10)

print(f"\n Top Skills for {selected_role}:")

for skill, count in ml_skill_counts:
    print(f"{skill}: {count}")


# --------------------------------------------------
# Visualization: Skills by Job Role
# --------------------------------------------------

if ml_skill_counts:

    role_skills = [item[0] for item in ml_skill_counts]
    role_counts = [item[1] for item in ml_skill_counts]

    plt.figure(figsize=(12, 6))

    bars = plt.bar(role_skills, role_counts)

    plt.title(f"Top Skills for {selected_role}")
    plt.xlabel("Skill")
    plt.ylabel("Number of Job Postings")

    plt.xticks(rotation=45, ha="right")

    for bar, count in zip(bars, role_counts):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f"{count:,}",
            ha="center",
            va="bottom"
        )

    plt.tight_layout()
    plt.show()

else:
    print(f"No data found for {selected_role}.")