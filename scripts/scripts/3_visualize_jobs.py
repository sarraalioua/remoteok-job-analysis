# =============================================================================
# PHASE 3 — Data Visualization for RemoteOK Jobs Dataset
# =============================================================================

import pandas as pd
import matplotlib.pyplot as plt
import os

# Load cleaned data
df = pd.read_csv("jobs_final_cleaned.csv", encoding="utf-8-sig")

print("Dataset shape:", df.shape)
print(df.head())

# Create folder for charts
output_folder = "charts"
os.makedirs(output_folder, exist_ok=True)


# =============================================================================
# 1. Top 10 Companies by Number of Job Offers
# =============================================================================

top_companies = df["company"].value_counts().head(10)

plt.figure(figsize=(10, 6))
top_companies.plot(kind="bar")
plt.title("Top 10 Companies by Number of Remote Job Offers")
plt.xlabel("Company")
plt.ylabel("Number of Jobs")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(f"{output_folder}/top_companies.png")
plt.show()


# =============================================================================
# 2. Top 10 Locations
# =============================================================================

top_locations = df["location"].value_counts().head(10)

plt.figure(figsize=(10, 6))
top_locations.plot(kind="bar")
plt.title("Top 10 Job Locations")
plt.xlabel("Location")
plt.ylabel("Number of Jobs")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(f"{output_folder}/top_locations.png")
plt.show()


# =============================================================================
# 3. Distribution of Number of Skills Required
# =============================================================================

plt.figure(figsize=(8, 5))
df["number_of_skills"].plot(kind="hist", bins=10)
plt.title("Distribution of Number of Skills Required per Job")
plt.xlabel("Number of Skills")
plt.ylabel("Number of Jobs")
plt.tight_layout()
plt.savefig(f"{output_folder}/skills_distribution.png")
plt.show()


# =============================================================================
# 4. Top 15 Required Skills
# =============================================================================

skills_series = df["skills"].dropna().str.split(",").explode()
skills_series = skills_series.str.strip()
skills_series = skills_series[skills_series != ""]

top_skills = skills_series.value_counts().head(15)

plt.figure(figsize=(10, 6))
top_skills.plot(kind="bar")
plt.title("Top 15 Most Required Skills")
plt.xlabel("Skill")
plt.ylabel("Frequency")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(f"{output_folder}/top_skills.png")
plt.show()


# =============================================================================
# 5. Jobs Posted Over Time
# =============================================================================

df["date_posted"] = pd.to_datetime(df["date_posted"], errors="coerce")

jobs_over_time = df.dropna(subset=["date_posted"])
jobs_over_time = jobs_over_time.groupby(jobs_over_time["date_posted"].dt.date).size()

plt.figure(figsize=(10, 5))
jobs_over_time.plot(kind="line", marker="o")
plt.title("Number of Jobs Posted Over Time")
plt.xlabel("Date")
plt.ylabel("Number of Jobs")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f"{output_folder}/jobs_over_time.png")
plt.show()


# =============================================================================
# 6. Remote Job Type Distribution
# =============================================================================

job_type_counts = df["job_type"].value_counts()

plt.figure(figsize=(7, 5))
job_type_counts.plot(kind="bar")
plt.title("Job Type Distribution")
plt.xlabel("Job Type")
plt.ylabel("Number of Jobs")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(f"{output_folder}/job_type_distribution.png")
plt.show()


# =============================================================================
# 7. Export Skills Frequency Table
# =============================================================================

skills_frequency = top_skills.reset_index()
skills_frequency.columns = ["skill", "frequency"]

skills_frequency.to_csv("skills_frequency.csv", index=False, encoding="utf-8-sig")

print("Phase 3 completed successfully.")
print("Charts saved in the 'charts' folder.")
print("skills_frequency.csv created successfully.")
