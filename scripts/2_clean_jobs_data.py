import pandas as pd
import re

# Load raw data
df = pd.read_csv("jobs_data.csv", encoding="utf-8-sig")

print("Raw shape:", df.shape)
print(df.head())

# Remove rows without title and company
df.dropna(subset=["title", "company"], how="all", inplace=True)

# Remove duplicate jobs
df.drop_duplicates(subset=["url"], keep="first", inplace=True)

# Clean text columns
text_columns = ["title", "company", "location", "job_type", "skills"]

for col in text_columns:
    df[col] = df[col].fillna("").astype(str).str.strip()

# Clean location
df["location"] = df["location"].replace("", "Remote")

# Clean remote column
df["remote"] = df["remote"].fillna(True).astype(bool)

# Clean salary
def clean_salary(salary):
    if pd.isna(salary) or str(salary).strip() == "":
        return None
    return str(salary).strip()

df["salary"] = df["salary"].apply(clean_salary)

# Extract numeric salary midpoint if possible
def parse_salary_midpoint(salary):
    if pd.isna(salary):
        return None

    salary = str(salary)
    numbers = re.findall(r"\d+", salary.replace(",", ""))

    if len(numbers) >= 2:
        return (float(numbers[0]) + float(numbers[1])) / 2
    elif len(numbers) == 1:
        return float(numbers[0])
    else:
        return None

df["salary_midpoint"] = df["salary"].apply(parse_salary_midpoint)

# Convert date
df["date_posted"] = pd.to_datetime(df["date_posted"], errors="coerce")

# Standardize skills
df["skills"] = df["skills"].fillna("").str.lower()

# Create number of skills column
def count_skills(skills):
    if skills == "":
        return 0
    return len([s for s in skills.split(",") if s.strip() != ""])

df["number_of_skills"] = df["skills"].apply(count_skills)

# Final column order
df = df[
    [
        "url",
        "title",
        "company",
        "location",
        "remote",
        "job_type",
        "date_posted",
        "skills",
        "number_of_skills"
    ]
]

print("Cleaned shape:", df.shape)
print(df.head())

df.to_csv("jobs_final_cleaned.csv", index=False, encoding="utf-8-sig")

print("jobs_final_cleaned.csv created successfully")
