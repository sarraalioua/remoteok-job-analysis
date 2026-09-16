# Remote Job Market Analytics Pipeline

Automated data engineering project extracting, cleaning, and visualizing remote job market trends from the RemoteOK API.

## 📊 Project Overview

This pipeline analyzes **99 remote job listings** across **95 companies** spanning **30 locations** to identify skills demand, hiring activity patterns, and salary trends in the remote work ecosystem.

### Key Metrics
- **99** total job postings collected
- **95** unique companies tracked
- **30** distinct job locations covered
- **10–12** average skills required per listing
- **~20** peak job postings in a single day (mid-April hiring surge)

## 🏗️ Architecture

The project follows a 3-layer data engineering workflow:

### Layer 1: Data Extraction (`1_extract_jobs.py`)
- Sends HTTP GET requests to RemoteOK API (`https://remoteok.com/api`)
- Adds custom User-Agent header (Mozilla/5.0) to simulate browser requests
- Parses JSON response and validates HTTP status (must be 200)
- Extracts 9 fields per job: `url`, `title`, `company`, `location`, `salary`, `date_posted`, `skills`, plus derived boolean `remote`
- Converts list of dictionaries → Pandas DataFrame
- Exports raw data as `jobs_raw.csv` (UTF-8 encoded)

**Output:** `data/jobs_raw.csv` (~99 rows)

### Layer 2: Data Cleaning & Transformation (`2_clean_jobs_data.py`)
- **Data Validation:** Drops rows missing title or company; removes duplicates by URL
- **Text Standardization:** Strips whitespace from 5 text columns; replaces empty locations with "Remote"
- **Boolean Handling:** Converts `remote` column to boolean type
- **Salary Processing:** 
  - Extracts salary midpoint from salary range strings using regex
  - If range exists → averages min/max; if single value → uses it directly
  - Returns `None` for unparseable entries
- **Date Conversion:** Converts ISO-formatted `date_posted` strings to datetime objects for time-series analysis
- **Feature Engineering:**
  - `number_of_skills` = counts comma-separated skill tags per job
  - Standardizes all text to lowercase

**Output:** `data/jobs_final_cleaned.csv` (~99 rows, 10 columns, fully typed)

### Layer 3: Analysis & Visualization (`3_visualize_jobs.py`)
- Loads cleaned dataset and performs exploratory data analysis (EDA)
- Generates 3 visualizations:
  1. **Posting Trend (Line Chart):** Job postings over time (April 18–25)
  2. **Skills Distribution (Histogram):** Count of skills per job (0–30 range)
  3. **Top Hiring Companies (Bar Chart):** Company vs. job count

**Dashboards:** Interactive Power BI dashboard (`dashboards/remoteok_dashboard.pbix`) with dynamic filters by Company, Location, Date Posted.

---

## 📈 Key Findings

1. **Remote Dominance:** 100% of 99 listings are fully remote positions
2. **Location Concentration:** 86.67% marked "Remote"; Canada, Los Angeles, and US locations each ~2.67%
3. **Skill Demand:** Most jobs require 5–15 skills; peak at 10–12 skills (moderate-to-high bar)
4. **Hiring Peak:** Burst of ~20 postings on April 22, followed by decline — suggests concentrated recruitment window
5. **Top Employers:** Pivotal Health, Adswerve Inc., Maneuver Marketing lead with 3 postings each; 12 companies contribute 1–2 roles

---

## 🛠️ Tech Stack

| Component | Tool |
|-----------|------|
| **API Client** | Python `requests` library |
| **Data Processing** | Pandas, NumPy |
| **Data Cleaning** | Regex (salary parsing), string methods |
| **Visualization** | Power BI (interactive dashboards) |
| **Data Format** | CSV (UTF-8), JSON (API response) |

---

## 🚀 How to Run

### Prerequisites
```bash
pip install pandas requests
```

### Execution (3-Step Pipeline)

**Step 1: Extract data from RemoteOK API**
```bash
python scripts/1_extract_jobs.py
# Output: data/jobs_raw.csv (99 rows)
```

**Step 2: Clean & transform**
```bash
python scripts/2_clean_jobs_data.py
# Output: data/jobs_final_cleaned.csv (fully typed, feature-engineered)
```

**Step 3: Analyze & export insights**
```bash
python scripts/3_visualize_jobs.py
# Output: outputs/skills_frequency.csv, console EDA stats
```

**Step 4: Open dashboard**
- Open `dashboards/remoteok_dashboard.pbix` in Power BI Desktop
- Use left-panel filters (Company, Location, Date Posted) to slice data dynamically

---

## 📁 Data Dictionary

| Field | Type | Source | Description |
|-------|------|--------|-------------|
| `url` | string | RemoteOK API | Direct link to job posting page |
| `title` | string | RemoteOK API | Job position title (e.g., "Data Analyst") |
| `company` | string | RemoteOK API | Hiring organization name |
| `location` | string | RemoteOK API | Job location (defaults to "Remote" if absent) |
| `salary` | string | RemoteOK API | Raw salary string (e.g., "$50K-$80K") |
| `salary_midpoint` | float | Derived | Calculated average of salary range (null if unparseable) |
| `date_posted` | datetime | RemoteOK API | ISO-formatted posting date, converted to datetime |
| `skills` | string | RemoteOK API | Comma-separated list of required skills/technologies |
| `number_of_skills` | integer | Derived | Count of skills per job |
| `remote` | boolean | Derived | True if position is fully remote |

---

## 💡 Use Cases

- **Job Seekers:** Identify in-demand skills and competitive salary ranges
- **Employers:** Benchmark hiring activity and skill requirements against peers
- **Researchers:** Analyze remote work market trends over time
- **Career Strategists:** Spot emerging technologies (e.g., trending skills) early

---

## 📊 Dashboard Features

The Power BI dashboard includes:

- **KPI Cards:** Total jobs, companies, and unique locations at a glance
- **Dynamic Filters:** Slice by Company, Location, Date Posted to zoom into subsets
- **Posting Trend:** Line chart showing hiring velocity over April 18–25
- **Skill Demand Distribution:** Histogram of skill counts (normal-like distribution, peak 10–12)
- **Top Hiring Companies:** Bar chart of companies by remote job volume
- **Geographic Breakdown:** Pie chart of job locations (Remote-heavy market)

---

## 🔄 Project Evolution

This project began as a web-scraper for Monster.com but pivoted to leverage the **RemoteOK public API** after discovering it provides structured job data without web-scraping overhead. The API-based approach is more maintainable, faster, and cleaner.

---

## 📝 Notes

- **Data Freshness:** Dataset captured April 18–25, 2025 (single snapshot)
- **API Rate Limits:** No authentication required; public endpoint at `https://remoteok.com/api`
- **Encoding:** All CSV files use UTF-8 (standard for international data)
- **Salary Parsing:** Handles ranges (e.g., "50-80") and single values; returns `None` for unparseable strings

---

## 👤 Author

Sarah Alioua | Business Analytics, Tunis Business School

---

## 📜 License

Open source for educational & research purposes.
