# Stage 3: Location Analysis

import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Load cleaned dataset
df = pd.read_csv("data_jobs_cleaned2.csv")

# 1. Job postings by city
city_counts = df["location_city"].value_counts()
print(" Job Postings by City:")
print(city_counts)

# 2. Job postings by state
state_counts = df["location_state"].value_counts()
print("\n Job Postings by State:")
print(state_counts)

# 3. Job postings by country
country_counts = df["location_country"].value_counts()
print("\n Job Postings by Country:")
print(country_counts)

# --- Visualizations ---

# Top 10 cities bar chart
top_cities = city_counts.head(10)
plt.figure(figsize=(10,5))
bars = plt.bar(top_cities.index, top_cities.values, color="skyblue")
plt.title("Top 10 Cities by Job Postings")
plt.xlabel("City")
plt.ylabel("Number of Postings")
plt.xticks(rotation=45)

# Add values on top of bars
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 200, yval, ha="center", va="bottom")

plt.tight_layout()
plt.show()

# Top 10 states bar chart
top_states = state_counts.head(10)
plt.figure(figsize=(10,5))
bars = plt.bar(top_states.index, top_states.values, color="lightgreen")
plt.title("Top 10 States by Job Postings")
plt.xlabel("State")
plt.ylabel("Number of Postings")
plt.xticks(rotation=45)

for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 200, yval, ha="center", va="bottom")

plt.tight_layout()
plt.show()

# Map visualization (Plotly)
fig = px.scatter_geo(df,
                     locations="location_country",
                     locationmode="country names",
                     title="Job Postings by Country",
                     hover_name="location_city",
                     size_max=20)
fig.show()
