# WikiWeak Article Finder

## Detecting Relatively Low-Content Wikipedia Articles Using Wikimedia Structured Data

WikiWeak Article Finder is a data science project that analyzes Wikipedia articles and identifies articles with relatively low content richness using structured information from Wikimedia's English Wikipedia dataset.

The project extracts measurable content factors such as article length, sections, infobox fields, images, and references. These factors are combined into a weighted content-richness score, which is then used to rank articles and identify relatively limited-content articles.

The results are presented through an interactive Streamlit dashboard.

> **Important:** The score used in this project is an experimental relative measure created for this project. It is **not an official Wikimedia or Wikipedia article-quality rating**.

---

## 📌 Problem Statement

Wikipedia contains millions of articles with large differences in the amount of available content.

Some articles may contain:

- Very little text
- Few or no sections
- Few or no images
- Limited infobox information
- Few references

Manually identifying such articles across a large dataset is difficult.

### Objective

Build a system that can:

1. Analyze multiple Wikipedia articles.
2. Extract measurable content-related factors.
3. Calculate a content-richness score.
4. Rank articles according to that score.
5. Identify articles with relatively limited content.
6. Display the factors responsible for each score.
7. Provide an interactive way to explore the results.

---

# 🔎 Our Approach

The project follows this pipeline:

```text
Wikimedia Structured Wikipedia Dataset
                ↓
        Select Article Sample
                ↓
       Extract Article Factors
                ↓
   ┌────────────┬────────────┬────────────┐
   │            │            │            │
 Length      Sections     Infoboxes     Images
   │            │            │            │
   └────────────┴────────────┴────────────┘
                    ↓
               References
                    ↓
          Calculate Percentiles
                    ↓
        Weighted Content Score
                    ↓
           Rank the Articles
                    ↓
       Identify Lowest-Scoring 5%
                    ↓
          Streamlit Dashboard
```

---

# 📊 Dataset

The project uses the:

**Wikipedia Structured Contents — English Wikipedia (`enwiki`)**

dataset provided by the Wikimedia Foundation / Wikimedia Enterprise through Kaggle.

The dataset contains structured information for millions of English Wikipedia articles.

Each article record can contain information such as:

- Article name
- Article URL
- Description
- Abstract
- Article version information
- Article length
- Images
- Infoboxes
- Sections
- Tables
- References

---

# 🧪 Sampling Method

The complete English Wikipedia dataset contains millions of article records and is too large to load completely into the available notebook memory.

Therefore, a memory-efficient sampling approach was used.

For each Parquet shard:

1. Up to 150 rows were read.
2. The sampled rows from all shards were combined.
3. A random sample of 10,000 articles was selected using seed `42`.

Therefore, the project analyzes a:

**10,000-article sample**

drawn from the Wikimedia structured dataset.

> This sampling method should not be interpreted as a perfectly uniform random sample of all English Wikipedia articles.

---

# 🧩 Features Extracted

The project uses five main measurable factors.

| Factor | Description | Weight |
|---|---|---:|
| Article Length | Number of characters in the article version | 40% |
| Section Count | Number of structured sections | 20% |
| Infobox Fields | Number of detected infobox fields | 10% |
| Images | Number of detected images | 10% |
| References | Number of references | 20% |

These factors provide measurable indicators of the amount of textual and structured content available in an article.

---

# 📐 Scoring Method

Different factors have different numerical ranges.

For example:

- Article length may contain thousands of characters.
- Sections may be counted in tens.
- Images may be few.
- References may vary widely.

To make these factors comparable, each factor is converted into a **percentile rank within the analyzed sample**.

The percentile values are then combined using weighted scoring.

### Formula

```text
Content Richness Score =
    (Length Percentile × 0.40)
  + (Section Percentile × 0.20)
  + (Infobox Percentile × 0.10)
  + (Image Percentile × 0.10)
  + (Reference Percentile × 0.20)
```

The weighted score is multiplied by 100.

```text
Final Score = Weighted Percentile Score × 100
```

The resulting score is approximately on a:

```text
0 – 100
```

scale.

---

# 📉 Identifying Relatively Limited-Content Articles

Instead of defining an arbitrary fixed score, the project uses the score distribution of the analyzed sample.

The bottom **5%** of the analyzed articles are classified as:

**Relatively limited-content articles**

For the current 10,000-article sample:

| Metric | Result |
|---|---:|
| Articles analyzed | 10,000 |
| Limited-content threshold | 11.76 / 100 |
| Articles identified | 502 |
| Lowest observed score | ~9.41 |

The count is 502 because articles at or below the calculated threshold are included.

---

# 📈 Current Results

Some of the lowest-scoring articles in the analyzed sample include:

| Article | Score | Characters | Sections | Infobox Fields | Images | References |
|---|---:|---:|---:|---:|---:|---:|
| Aşağıçavuş | 9.41 | 91 | 1 | 0 | 0 | 0 |
| Oswell | 9.41 | 88 | 1 | 0 | 0 | 0 |
| Tarao Naga | 9.42 | 95 | 1 | 0 | 0 | 0 |
| Kambaata | 9.42 | 94 | 1 | 0 | 0 | 0 |
| Weston Fen | 9.43 | 98 | 1 | 0 | 0 | 0 |

These examples demonstrate how the scoring system identifies articles containing very limited measurable content within the analyzed sample.

---

# 🖥️ Interactive Dashboard

The project includes an interactive Streamlit dashboard.

### 📊 Dataset Summary

The dashboard displays:

- Number of articles analyzed
- Number of limited-content articles
- Score threshold
- Current filtered results

### 🔍 Article Search

Users can search for a specific article by name.

Example:

```text
Oswell
```

### 🎚️ Score Filtering

Users can adjust the maximum content-richness score to explore different portions of the dataset.

### 📋 Results Table

The dashboard displays:

- Rank
- Article name
- Content-richness score
- Article length
- Section count
- Infobox fields
- Images
- References

### 📈 Score Distribution

A histogram shows how content-richness scores are distributed across the analyzed sample.

### 📉 Lowest-Scoring Articles

The dashboard displays articles with the lowest calculated scores.

### 🔎 Article Inspector

A selected article can be inspected individually to see the factors contributing to its score.

### 📥 CSV Export

Filtered results can be downloaded as a CSV file directly from the dashboard.

---

# 🧮 Example Score Breakdown

Example article: **Oswell**

| Factor | Value |
|---|---:|
| Article Length | 88 characters |
| Sections | 1 |
| Infobox Fields | 0 |
| Images | 0 |
| References | 0 |
| Content Score | 9.41 |

The low score results from low percentile values across the measured content factors.

---

# 🏗️ Project Architecture

```text
                 Wikimedia Dataset
                        │
                        ▼
                  Parquet Files
                        │
                        ▼
             Memory-Efficient Sampling
                        │
                        ▼
                 Feature Extraction
                        │
          ┌─────────────┼─────────────┐
          ▼             ▼             ▼
       Length        Sections      Infoboxes
          │             │             │
          └─────────────┼─────────────┘
                        │
                 Images + References
                        │
                        ▼
                Percentile Ranking
                        │
                        ▼
             Weighted Scoring Model
                        │
                        ▼
                  Article Ranking
                        │
                        ▼
               Bottom 5% Detection
                        │
                        ▼
                   Results CSV
                        │
                        ▼
                Streamlit Dashboard
```

---

# 🛠️ Technology Stack

### Programming Language

- Python

### Data Processing

- Polars
- Pandas

### Visualization & Dashboard

- Streamlit
- Matplotlib

### Dataset Format

- Apache Parquet
- JSON structured fields

### Development Environment

- Kaggle Notebooks
- Visual Studio Code

### Data Source

- Wikimedia Structured Contents
- English Wikipedia (`enwiki`)

---

# 📁 Repository Structure

```text
WikiWeak-Article-Finder/
│
├── app.py
├── notebook41a4210044.ipynb
├── wikiweak_results.csv
└── README.md
```

### `app.py`

Contains the Streamlit dashboard application.

### `notebook41a4210044.ipynb`

Contains the dataset processing, feature extraction, scoring, ranking, and analysis workflow.

### `wikiweak_results.csv`

Contains the generated results from the 10,000-article analysis.

### `README.md`

Contains project documentation.

---

# 🚀 How to Run Locally

## 1. Clone the Repository

```bash
git clone https://github.com/Saksham-M4/WikiWeak-Article-Finder.git
```

Move into the project directory:

```bash
cd WikiWeak-Article-Finder
```

## 2. Create a Virtual Environment

```bash
python3 -m venv .venv
```

Activate it on macOS/Linux:

```bash
source .venv/bin/activate
```

## 3. Install Required Packages

```bash
pip install streamlit pandas matplotlib
```

## 4. Run the Dashboard

```bash
streamlit run app.py
```

The dashboard will open in the browser.

If it does not open automatically, Streamlit normally provides a local address such as:

```text
http://localhost:8501
```

---

# 🔁 Reproducibility

The analysis uses a fixed random seed:

```python
seed=42
```

This makes the final 10,000-article sample reproducible when the same shard-selection procedure and dataset version are used.

The dataset processing was performed in Kaggle because the complete Wikimedia dataset is very large.

The generated CSV is included in this repository so that the Streamlit dashboard can run without requiring users to download the full Wikimedia dataset.

---

# ⚠️ Limitations

This project is an experimental data-analysis system and has several limitations.

### 1. Sample-Based Analysis

Only 10,000 articles were analyzed instead of the entire English Wikipedia dataset.

### 2. Sampling Method

The sample was constructed by taking up to 150 rows from each Parquet shard and then randomly selecting 10,000 rows.

Therefore, it should not be treated as a perfectly representative random sample of all Wikipedia articles.

### 3. Content Richness Is Not Article Quality

A low content-richness score does not necessarily mean that an article is incorrect, unimportant, or poorly written.

A short article can still provide useful information.

### 4. Experimental Score

The weights used in this project were chosen for the purposes of this prototype:

| Factor | Weight |
|---|---:|
| Article Length | 40% |
| Sections | 20% |
| Infobox Fields | 10% |
| Images | 10% |
| References | 20% |

They are not official Wikimedia weights.

### 5. Structured Data Limitations

Some fields in the dataset are stored as nested JSON structures. The project therefore uses parsing and counting rules to extract measurable factors.

### 6. Relative Ranking

Because the score is percentile-based, the score describes an article's position relative to the analyzed sample rather than providing an absolute measure of article quality.

---

# 🔮 Future Improvements

Possible future improvements include:

- Analyze a larger portion of the Wikimedia dataset.
- Improve the sampling methodology.
- Add additional content-quality indicators.
- Include table counts.
- Analyze reference quality and diversity.
- Detect extremely short articles separately.
- Add category-wise comparisons.
- Add filtering by article type or topic.
- Add time-based analysis using article versions.
- Compare scores across different dataset snapshots.
- Improve the scoring model using validated quality indicators.
- Deploy the dashboard publicly.

---

# 🎯 Project Outcome

WikiWeak Article Finder demonstrates how a large structured Wikipedia dataset can be transformed into an interactive data-analysis application.

The project combines:

```text
Large-Scale Dataset
        +
Data Processing
        +
Feature Engineering
        +
Percentile-Based Scoring
        +
Ranking
        +
Interactive Visualization
```

The resulting system provides a practical way to explore articles that contain relatively limited measurable content within the analyzed sample.

---

# 🌐 Project Repository

GitHub:

https://github.com/Saksham-M4/WikiWeak-Article-Finder

---

# 👤 Author

**Saksham Kumar**

Areas of interest:

- Open Source
- Wikimedia Projects
- Data Science
- Artificial Intelligence
- Software Development
- Practical Technology Projects

---

# 📜 Disclaimer

WikiWeak Article Finder is an educational and experimental data-science project.

The content-richness score is created specifically for this project and should not be interpreted as an official Wikipedia or Wikimedia quality assessment.

A low score only indicates relatively limited measurable content according to the selected factors and scoring method.

---

# 🙏 Acknowledgements

This project uses structured Wikipedia data provided through the Wikimedia ecosystem.

Special thanks to the organizers of the Open Source Day / WikiClub Tech event for providing the opportunity to work with Wikimedia structured data and explore open-source technologies.

---

# ⭐ Summary

WikiWeak Article Finder analyzes 10,000 sampled English Wikipedia articles, extracts measurable content features, calculates a percentile-based content-richness score, identifies the bottom 5% of the analyzed sample, and presents the results through an interactive Streamlit dashboard.

### Core Idea

```text
Analyze → Measure → Score → Rank → Explore
```

### WikiWeak Article Finder

```text
Find relatively low-content articles
              ↓
Using measurable structured-data factors
              ↓
With transparent scoring
              ↓
Through an interactive dashboard
```

---

## ⭐ Project Status

**Completed Prototype**

The project includes:

- Dataset analysis
- Feature extraction
- Content-richness scoring
- Article ranking
- Limited-content detection
- Results CSV
- Interactive Streamlit dashboard
- Search and filtering
- Article score inspection
- CSV export
- Complete project documentation

