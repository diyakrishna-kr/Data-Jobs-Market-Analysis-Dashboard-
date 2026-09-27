# Stage 3: Job Demand Analysis (with values on bars)

import pandas as pd
import matplotlib.pyplot as plt

# Load cleaned dataset
df = pd.read_csv("data_jobs_cleaned2.csv")

# 1. Top 10 job roles by postings
top_roles = df["job_title"].value_counts().head(10)
print(" Top 10 Job Roles by Number of Postings:")
print(top_roles)

# 2. Job postings by job category
category_counts = df["job_category"].value_counts()
print("\n Job Postings by Category:")
print(category_counts)

# 3. Job postings by employment type
employment_counts = df["employment_type"].value_counts()
print("\n Job Postings by Employment Type:")
print(employment_counts)

# 4. Total job postings
total_postings = len(df)
print("\n Total Job Postings:", total_postings)

# 5. Unique companies
unique_companies = df["company_name"].nunique()
print(" Unique Companies:", unique_companies)

# 6. Unique locations (city-level)
unique_locations = df["location_city"].nunique()
print(" Unique Locations (Cities):", unique_locations)

# --- Visualizations ---

# Top 10 job roles bar chart
plt.figure(figsize=(10,5))
bars = plt.bar(top_roles.index, top_roles.values, color="skyblue")
plt.title("Top 10 Job Roles by Number of Postings")
plt.xlabel("Job Role")
plt.ylabel("Number of Postings")
plt.xticks(rotation=45)

# Add values on top of bars
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 200, yval, ha="center", va="bottom")

plt.tight_layout()
plt.show()

# Job category pie chart
plt.figure(figsize=(6,6))
category_counts.plot(kind="pie", autopct="%1.1f%%", startangle=90, colors=plt.cm.Paired.colors)
plt.title("Job Postings by Category")
plt.ylabel("")
plt.show()

# Employment type bar chart
plt.figure(figsize=(8,5))
bars = plt.bar(employment_counts.index, employment_counts.values, color="lightgreen")
plt.title("Job Postings by Employment Type")
plt.xlabel("Employment Type")
plt.ylabel("Number of Postings")
plt.xticks(rotation=45)

# Add values on top of bars
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 200, yval, ha="center", va="bottom")

plt.tight_layout()
plt.show()
