# Stage 3: Salary Analysis 
 
import pandas as pd 
import matplotlib.pyplot as plt 
 
# Load cleaned dataset 
df = pd.read_csv("data_jobs_cleaned2.csv") 
 
# 1. Average salary by job role 
df["avg_salary"] = (df["salary_minimum"] + df["salary_maximum"]) / 2 
avg_salary_roles = df.groupby("job_title")["avg_salary"].mean().sort_values(ascending=False).head(10) 
print(" Average Salary by Job Role (Top 10):") 
print(avg_salary_roles) 
 
# 2. Salary distribution by job category 
avg_salary_category = df.groupby("job_category")["avg_salary"].mean().sort_values(ascending=False) 
print("\n Average Salary by Job Category:") 
print(avg_salary_category) 
 
# 3. Salary by employment type 
avg_salary_employment = df.groupby("employment_type")["avg_salary"].mean() 
print("\n Average Salary by Employment Type:") 
print(avg_salary_employment) 
 
# 4. Overall salary KPIs 
print("\n Salary KPIs:") 
print("Minimum Salary:", df["salary_minimum"].min()) 
print("Maximum Salary:", df["salary_maximum"].max()) 
print("Mean Salary:", round(df["avg_salary"].mean(), 2)) 
print("Median Salary:", df["avg_salary"].median()) 
 
# --- Visualizations --- 
 
# Average salary by job role (Top 10) 
plt.figure(figsize=(10,5)) 
bars = plt.bar(avg_salary_roles.index, avg_salary_roles.values / 100000, color="orange") 
plt.title("Average Salary by Job Role (Top 10)") 
plt.xlabel("Job Role") 
plt.ylabel("Average Salary (₹ Lakhs)") 
plt.xticks(rotation=45) 
 
# Add values on top of bars 
for bar in bars: 
    yval = bar.get_height() 
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.05, f"{yval:.2f}L", ha="center", va="bottom") 
 
plt.tight_layout() 
plt.show() 
 
# Salary distribution by job category 
plt.figure(figsize=(8,5)) 
bars = plt.bar(avg_salary_category.index, avg_salary_category.values / 100000, color="purple") 
plt.title("Average Salary by Job Category") 
plt.xlabel("Job Category") 
plt.ylabel("Average Salary (₹ Lakhs)") 
plt.xticks(rotation=45) 
 
for bar in bars: 
    yval = bar.get_height() 
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.05, f"{yval:.2f}L", ha="center", va="bottom") 
 
plt.tight_layout() 
plt.show() 
 
# Salary by employment type 
plt.figure(figsize=(6,4)) 
bars = plt.bar(avg_salary_employment.index, avg_salary_employment.values / 100000, color="green") 
plt.title("Average Salary by Employment Type") 
plt.xlabel("Employment Type") 
plt.ylabel("Average Salary (₹ Lakhs)") 
 
for bar in bars: 
    yval = bar.get_height() 
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.05, f"{yval:.2f}L", ha="center", va="bottom") 
 
plt.tight_layout() 
plt.show()




'''python -m streamlit run dash.py'''

















































































































































'''# Stage 3: Salary Analysis

import pandas as pd
import matplotlib.pyplot as plt

# Load cleaned dataset
df = pd.read_csv("data_jobs_cleaned2.csv")

# 1. Average salary by job role
df["avg_salary"] = (df["salary_minimum"] + df["salary_maximum"]) / 2
avg_salary_roles = df.groupby("job_title")["avg_salary"].mean().sort_values(ascending=False).head(10)
print("🔹 Average Salary by Job Role (Top 10):")
print(avg_salary_roles)

# 2. Salary distribution by job category
avg_salary_category = df.groupby("job_category")["avg_salary"].mean().sort_values(ascending=False)
print("\n🔹 Average Salary by Job Category:")
print(avg_salary_category)

# 3. Salary by employment type
avg_salary_employment = df.groupby("employment_type")["avg_salary"].mean()
print("\n🔹 Average Salary by Employment Type:")
print(avg_salary_employment)

# 4. Overall salary KPIs
print("\n🔹 Salary KPIs:")
print("Minimum Salary:", df["salary_minimum"].min())
print("Maximum Salary:", df["salary_maximum"].max())
print("Mean Salary:", round(df["avg_salary"].mean(), 2))
print("Median Salary:", df["avg_salary"].median())

# --- Visualizations ---

# Average salary by job role (Top 10)
plt.figure(figsize=(10,5))
bars = plt.bar(avg_salary_roles.index, avg_salary_roles.values, color="orange")
plt.title("Average Salary by Job Role (Top 10)")
plt.xlabel("Job Role")
plt.ylabel("Average Salary")
plt.xticks(rotation=45)

# Add values on top of bars
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 500, round(yval, 0), ha="center", va="bottom")

plt.tight_layout()
plt.show()

# Salary distribution by job category
plt.figure(figsize=(8,5))
bars = plt.bar(avg_salary_category.index, avg_salary_category.values, color="purple")
plt.title("Average Salary by Job Category")
plt.xlabel("Job Category")
plt.ylabel("Average Salary")
plt.xticks(rotation=45)

for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 500, round(yval, 0), ha="center", va="bottom")

plt.tight_layout()
plt.show()

# Salary by employment type
plt.figure(figsize=(6,4))
bars = plt.bar(avg_salary_employment.index, avg_salary_employment.values, color="green")
plt.title("Average Salary by Employment Type")
plt.xlabel("Employment Type")
plt.ylabel("Average Salary")

for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 500, round(yval, 0), ha="center", va="bottom")

plt.tight_layout()
plt.show()
'''