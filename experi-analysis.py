# Stage 3: Experience Analysis

import pandas as pd
import matplotlib.pyplot as plt

# Load cleaned dataset
df = pd.read_csv("data_jobs_cleaned2.csv")

# 1. Job postings by experience level
experience_counts = df["experience_level"].value_counts()
print(" Job Postings by Experience Level:")
print(experience_counts)

# 2. Salary trend by experience level
df["avg_salary"] = (df["salary_minimum"] + df["salary_maximum"]) / 2
salary_by_experience = df.groupby("experience_level")["avg_salary"].mean().sort_values()
print("\n Average Salary by Experience Level:")
print(salary_by_experience)

# --- Visualizations ---

# Bar chart: Job postings by experience level
plt.figure(figsize=(8,5))
bars = plt.bar(experience_counts.index, experience_counts.values, color="skyblue")
plt.title("Job Postings by Experience Level")
plt.xlabel("Experience Level")
plt.ylabel("Number of Postings")
plt.xticks(rotation=45)

# Add values on top of bars
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 200, yval, ha="center", va="bottom")

plt.tight_layout()
plt.show()

# Line chart: Salary trend by experience level
plt.figure(figsize=(8,5))
plt.plot(salary_by_experience.index, salary_by_experience.values, marker="o", color="green")
plt.title("Salary Trend by Experience Level")
plt.xlabel("Experience Level")
plt.ylabel("Average Salary")
plt.xticks(rotation=45)

# Add values on each point
for i, val in enumerate(salary_by_experience.values):
    plt.text(i, val + 500, round(val, 0), ha="center")

plt.tight_layout()
plt.show()
