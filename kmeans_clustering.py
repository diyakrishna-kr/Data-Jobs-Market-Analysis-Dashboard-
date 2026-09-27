# ============================================================
# Stage 4: K-Means Clustering
# Data Jobs Market Analysis
# ============================================================

import pandas as pd
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans


# ============================================================
# 1. LOAD DATASET
# ============================================================

df = pd.read_csv("data_jobs_cleaned2.csv")

print("=" * 60)
print("K-MEANS CLUSTERING")
print("=" * 60)

print("\nDataset Shape:")
print(df.shape)

print("\nAvailable Columns:")
print(df.columns.tolist())


# ============================================================
# 2. CHECK REQUIRED COLUMNS
# ============================================================

required_columns = [
    "salary_minimum",
    "salary_maximum",
    "career_growth_index",
    "experience_level",
    "skill_count"
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:
    print("\nERROR: The following columns are missing:")
    print(missing_columns)
    print("\nPlease check your dataset column names.")
    exit()


# ============================================================
# 3. CREATE AVERAGE SALARY
# ============================================================

df["avg_salary"] = (
    df["salary_minimum"] + df["salary_maximum"]
) / 2

print("\n" + "=" * 60)
print("AVERAGE SALARY")
print("=" * 60)

print("\nAverage salary column created successfully.")

print("\nSample salary data:")

print(
    df[
        ["salary_minimum", "salary_maximum", "avg_salary"]
    ].head()
)


# ============================================================
# 4. CONVERT EXPERIENCE LEVEL TO NUMERIC
# ============================================================

print("\n" + "=" * 60)
print("EXPERIENCE LEVEL CONVERSION")
print("=" * 60)

print("\nOriginal Experience Levels:")
print(df["experience_level"].value_counts())


# Actual values in your dataset
experience_mapping = {
    "Freshers / Entry Level": 0,
    "Mid-Senior Level": 1
}

df["experience_level_numeric"] = (
    df["experience_level"]
    .astype(str)
    .str.strip()
    .map(experience_mapping)
)

print("\nConverted Experience Levels:")

print(
    df[
        ["experience_level", "experience_level_numeric"]
    ].drop_duplicates()
)


# ============================================================
# 5. SELECT FEATURES
# ============================================================

print("\n" + "=" * 60)
print("FEATURE SELECTION")
print("=" * 60)

features = [
    "avg_salary",
    "career_growth_index",
    "experience_level_numeric",
    "skill_count"
]

print("\nFeatures selected for K-Means:")

print(features)


# ============================================================
# 6. CHECK MISSING VALUES
# ============================================================

print("\n" + "=" * 60)
print("MISSING VALUE CHECK")
print("=" * 60)

print("\nMissing values before cleaning:")

print(
    df[features].isnull().sum()
)


# ============================================================
# 7. REMOVE ROWS WITH MISSING VALUES
# ============================================================

df_clustering = df.dropna(
    subset=features
).copy()

print("\nOriginal rows:", len(df))

print(
    "Rows used for clustering:",
    len(df_clustering)
)

print(
    "Rows removed:",
    len(df) - len(df_clustering)
)


# ============================================================
# 8. PREPARE FEATURES
# ============================================================

X = df_clustering[features]

print("\nFeature data:")

print(X.head())


# ============================================================
# 9. SCALE FEATURES
# ============================================================

print("\n" + "=" * 60)
print("FEATURE SCALING")
print("=" * 60)

scaler = StandardScaler()

scaled_features = scaler.fit_transform(X)

print("\nFeatures scaled successfully.")


# ============================================================
# 10. ELBOW METHOD
# ============================================================

print("\n" + "=" * 60)
print("ELBOW METHOD")
print("=" * 60)

inertia = []

for k in range(2, 11):

    model = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )

    model.fit(scaled_features)

    inertia.append(model.inertia_)


print("\nInertia values:")

for k, value in zip(range(2, 11), inertia):

    print(
        f"K = {k} : Inertia = {value:.2f}"
    )


# Plot Elbow Method

plt.figure(figsize=(8, 5))

plt.plot(
    range(2, 11),
    inertia,
    marker="o"
)

plt.title(
    "Elbow Method for Choosing K"
)

plt.xlabel(
    "Number of Clusters (K)"
)

plt.ylabel(
    "Inertia"
)

plt.xticks(range(2, 11))

plt.grid(True)

plt.tight_layout()

plt.show()


# ============================================================
# 11. SELECT NUMBER OF CLUSTERS
# ============================================================

# Start with 4 clusters.
# Change this after checking the elbow graph.

chosen_k = 4

print("\n" + "=" * 60)
print("SELECTED NUMBER OF CLUSTERS")
print("=" * 60)

print(
    f"\nNumber of clusters selected: {chosen_k}"
)


# ============================================================
# 12. TRAIN K-MEANS
# ============================================================

print("\n" + "=" * 60)
print("TRAINING K-MEANS")
print("=" * 60)

kmeans = KMeans(
    n_clusters=chosen_k,
    random_state=42,
    n_init=10
)

df_clustering["cluster"] = (
    kmeans.fit_predict(scaled_features)
)

print(
    "\nK-Means clustering completed successfully."
)


# ============================================================
# 13. CLUSTER COUNTS
# ============================================================

print("\n" + "=" * 60)
print("JOBS IN EACH CLUSTER")
print("=" * 60)

cluster_counts = (
    df_clustering["cluster"]
    .value_counts()
    .sort_index()
)

print(cluster_counts)


# ============================================================
# 14. CLUSTER SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("CLUSTER SUMMARY")
print("=" * 60)

cluster_summary = (
    df_clustering
    .groupby("cluster")[
        [
            "avg_salary",
            "career_growth_index",
            "experience_level_numeric",
            "skill_count"
        ]
    ]
    .mean()
    .round(2)
)

print("\nAverage characteristics of each cluster:")

print(cluster_summary)


# ============================================================
# 15. ADD CLUSTER TO ORIGINAL DATASET
# ============================================================

df.loc[
    df_clustering.index,
    "cluster"
] = df_clustering["cluster"]

df["cluster"] = df["cluster"].astype("Int64")


# ============================================================
# 16. SAVE CLUSTERED DATASET
# ============================================================

output_file = "data_jobs_clustered.csv"

df.to_csv(
    output_file,
    index=False
)

print("\n" + "=" * 60)
print("FILE SAVED")
print("=" * 60)

print(
    f"\nClustered dataset saved as: {output_file}"
)


# ============================================================
# 17. CLUSTER VISUALIZATION
# ============================================================

plt.figure(figsize=(10, 6))

for cluster in sorted(
    df_clustering["cluster"].unique()
):

    cluster_data = df_clustering[
        df_clustering["cluster"] == cluster
    ]

    plt.scatter(
        cluster_data["career_growth_index"],
        cluster_data["avg_salary"],
        label=f"Cluster {cluster}"
    )


plt.title(
    "Job Clusters: Salary vs Career Growth"
)

plt.xlabel(
    "Career Growth Index"
)

plt.ylabel(
    "Average Salary"
)

plt.legend()

plt.grid(True)

plt.tight_layout()

plt.show()


# ============================================================
# 18. FINAL OUTPUT
# ============================================================

print("\n" + "=" * 60)
print("K-MEANS CLUSTERING COMPLETED")
print("=" * 60)

print("\nFinal dataset shape:")
print(df.shape)

print("\nCluster distribution:")
print(
    df["cluster"]
    .value_counts()
    .sort_index()
)

print("\nCluster summary:")
print(cluster_summary)

print("\nOutput file:")
print(output_file)