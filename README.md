

# 📚 WikiWeak Article Finder

## Detecting Relatively Limited-Content Wikipedia Articles Using Wikimedia Structured Data

WikiWeak Article Finder is an experimental data-analysis project that analyzes Wikipedia articles and identifies articles with **relatively limited measurable content** using structured information from Wikimedia's English Wikipedia dataset.

The system measures five content-related factors:

- **Word Count**
- **Section Count**
- **Infobox Fields**
- **Images**
- **References**

These factors are converted into percentile values within the analyzed sample and combined using transparent weights to produce an experimental **content-richness score**.

The results are presented through an interactive **Streamlit dashboard**.

> **Important:** The score is an experimental relative measure created for this project. It is **not an official Wikimedia or Wikipedia article-quality rating**.

---

# 🎯 Problem Statement

Wikipedia contains a very large number of articles with substantial differences in the amount of available content.

Some articles may contain:

- Very little text
- Few or no sections
- Few or no images
- Limited infobox information
- Few references

Manually identifying such articles across a large dataset is difficult.

## Objective

The project aims to:

1. Analyze multiple Wikipedia articles.
2. Extract measurable content-related factors.
3. Calculate an experimental content-richness score.
4. Rank articles according to that score.
5. Identify articles with relatively limited measurable content.
6. Show the actual factors behind each result.
7. Explain how the score is calculated.
8. Provide an interactive dashboard for exploration.

---

# 🔎 Core Approach

The project follows this pipeline:

```text
Wikimedia Structured Wikipedia Dataset
                ↓
        Select Article Sample
                ↓
        Extract Content Factors
                ↓
 ┌──────────┬──────────┬──────────┬──────────┐
 │          │          │          │          │
Word Count Sections  Infoboxes   Images   References
 │          │          │          │          │
 └──────────┴──────────┴──────────┴──────────┘
                ↓
        Calculate Percentiles
                ↓
      Apply Transparent Weights
                ↓
     Content-Richness Score
                ↓
        Rank the Articles
                ↓
   Identify Relatively Limited
          Content Articles
                ↓
        Streamlit Dashboard
```

### Important design principle

An article is **not** considered limited-content because of one factor alone.

The result is based on the **combined behavior of five measurable content factors**.

---

# 📊 Dataset

The project uses:

**Wikipedia Structured Contents — English Wikipedia (`enwiki`)**

The dataset is provided through the Wikimedia ecosystem.

Article records can contain structured information such as:

- Article name
- Article URL
- Description
- Abstract
- Article version information
- Article text/content information
- Images
- Infoboxes
- Sections
- Tables
- References

---

# 🧪 Sampling Method

The complete English Wikipedia dataset contains millions of article records and is too large to load completely into the available notebook environment.

Therefore, a memory-efficient sampling approach was used.

For each Parquet shard:

1. Up to 150 rows were read.
2. The sampled rows from the shards were combined.
3. A random sample of **10,000 articles** was selected using seed `42`.

Therefore, the current project analyzes:

> **10,000 sampled Wikipedia articles**

This should not be interpreted as a perfectly uniform random sample of all English Wikipedia articles.

---

# 🧩 Five Content Factors

The project uses five measurable factors:

| Factor | What it measures | Weight |
|---|---|---:|
| **Word Count** | Number of words in the available article content | **40%** |
| **Section Count** | Number of structured sections | **20%** |
| **References** | Number of detected references | **20%** |
| **Infobox Fields** | Number of detected infobox fields | **10%** |
| **Images** | Number of detected images | **10%** |

These factors are used together to estimate the amount of measurable content available in an article.

> **Note:** The weights are experimental project choices and are not official Wikimedia weights.

---

# 📐 Scoring Method

The five factors have different numerical ranges.

For example:

- Word counts can vary substantially.
- Sections may be counted in tens.
- Images may be relatively few.
- References can vary widely.
- Infobox fields can also vary between articles.

To make the factors comparable, each factor is converted into a **percentile rank within the analyzed sample**.

The percentile values are then combined using the displayed weights.

## Formula

```text
Content-Richness Score =
    (Word Count Percentile × 0.40)
  + (Section Percentile × 0.20)
  + (Infobox Percentile × 0.10)
  + (Image Percentile × 0.10)
  + (Reference Percentile × 0.20)
```

```text
Final Score = Weighted Percentile Score × 100
```

The resulting score is approximately on a:

```text
0 – 100
```

scale.

### Interpretation

A higher score means the article has relatively higher measured content across the selected factors within the analyzed sample.

A lower score means the article has relatively lower measured content across the selected factors within the analyzed sample.

The score is **relative**, not an absolute measure of article quality.

---

# 📉 Identifying Relatively Limited-Content Articles

Instead of using an arbitrary universal score, the project uses the distribution of scores in the analyzed sample.

The lowest **5%** of the analyzed articles are identified as:

> **Relatively limited-content articles**

For the current 10,000-article sample:

| Metric | Result |
|---|---:|
| Articles analyzed | 10,000 |
| Limited-content threshold | 11.76 / 100 |
| Articles identified | 502 |
| Lowest observed score | ~9.41 |

Articles at or below the calculated threshold are included in the limited-content group.

> This is an experimental project classification based on the selected factors and sample. It is **not an official Wikimedia classification**.

---

# 🔎 Why an Article Is Considered Relatively Limited-Content

For every selected article, the dashboard displays the actual values of the five factors.

Example:

```text
Article: Example Article

Word Count:       107
Sections:           1
Infobox Fields:     0
Images:             0
References:         0

Content-Richness Score: 9.43 / 100
```

The dashboard also displays:

- Relative percentile for each factor
- Weight assigned to each factor
- Weighted contribution
- Final score

This allows the user to understand **why the score is relatively low**.

### Important

The application does **not** decide that an article is limited-content from word count alone.

Instead:

```text
Word Count
     +
Sections
     +
Infobox Fields
     +
Images
     +
References
     ↓
Combined Content-Richness Score
```

This makes the result transparent and explainable.

---

# 🖥️ Interactive Streamlit Dashboard

The project includes an interactive Streamlit dashboard.

## 📊 Dataset Summary

The dashboard displays:

- Number of articles analyzed
- Number of limited-content articles
- Score threshold
- Number of scoring factors
- Current filtered results

## 🔍 Article Search

Users can search for a specific article by name.

Example:

```text
Oswell
```

## 🎚️ Score Filtering

Users can adjust the maximum content-richness score to explore different portions of the analyzed dataset.

## 📋 Article Results

The dashboard displays:

- Article name
- Content-richness score
- Word Count
- Section Count
- Infobox Fields
- Images
- References

## 📈 Score Distribution

A histogram shows how content-richness scores are distributed across the analyzed sample.

## 📉 Lowest Content-Richness Scores

The dashboard displays articles with the lowest calculated scores.

## 🔎 Article Inspector

A selected article can be inspected individually.

The inspector shows:

- Actual factor values
- Relative percentiles
- Scoring weights
- Weighted contributions
- Final content-richness score
- Explanation of why the score is relatively low

## 📥 CSV Export

Filtered results can be downloaded directly from the dashboard.

---

# 🧮 Example Score Breakdown

Example article: **Oswell**

| Factor | Value |
|---|---:|
| Word Count | 107 |
| Sections | 1 |
| Infobox Fields | 0 |
| Images | 0 |
| References | 0 |
| Content Score | 9.41 |

The score is produced from the **combined percentile values of all five factors**.

Therefore, the application does not claim that the article is limited-content because of one missing feature. It identifies relatively limited measurable content based on the combined scoring model.

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
       ┌───────────────┼────────────────┐
       ▼               ▼                ▼
   Word Count       Sections         Infoboxes
       │               │                │
       └───────────────┼────────────────┘
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

### Dashboard & Visualization

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

### Analysis notebook

Contains the dataset processing, feature extraction, scoring, ranking, and analysis workflow.

### `wikiweak_results.csv`

Contains the generated results from the 10,000-article analysis.

### `README.md`

Contains project documentation and methodology.

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

The dashboard will normally be available at:

```text
http://localhost:8501
```

---

# 🔁 Reproducibility

The analysis uses a fixed random seed:

```python
seed=42
```

This helps reproduce the same 10,000-article sample when the same dataset version and sampling procedure are used.

The large dataset was processed in Kaggle because the complete Wikimedia dataset is very large.

The generated CSV is included in the repository so that the Streamlit dashboard can run without requiring users to download the full dataset.

---

# ⚠️ Limitations

## 1. Sample-Based Analysis

Only 10,000 articles were analyzed instead of the entire English Wikipedia dataset.

## 2. Sampling Method

The sample was constructed by taking up to 150 rows from each Parquet shard and then randomly selecting 10,000 rows.

Therefore, it should not be treated as a perfectly representative random sample of all Wikipedia articles.

## 3. Content Richness Is Not Article Quality

A low content-richness score does **not** necessarily mean that an article is:

- Incorrect
- Unimportant
- Poorly written
- In need of deletion

A short article can still provide useful information.

## 4. Experimental Score

The weights used in this project were chosen for the purposes of this prototype:

| Factor | Weight |
|---|---:|
| Word Count | 40% |
| Sections | 20% |
| References | 20% |
| Infobox Fields | 10% |
| Images | 10% |

These are **not official Wikimedia weights**.

## 5. Structured Data Limitations

Some dataset fields are stored as nested structured data. Parsing and counting rules are therefore used to extract measurable factors.

## 6. Relative Ranking

Because the score is percentile-based, it describes an article's position relative to the analyzed sample rather than providing an absolute measure of article quality.

---

# 🔮 Future Improvements

Possible future improvements include:

- Analyze a larger portion of the Wikimedia dataset.
- Improve the sampling methodology.
- Add additional content-richness indicators.
- Include table counts.
- Analyze reference quality and diversity.
- Detect extremely short articles separately.
- Add category-wise comparisons.
- Add filtering by article type or topic.
- Add time-based analysis using article versions.
- Compare scores across different dataset snapshots.
- Improve the scoring model using validated indicators.
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

The resulting system provides a transparent way to explore Wikipedia articles that contain **relatively limited measurable content within the analyzed sample**.

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

WikiWeak Article Finder analyzes 10,000 sampled English Wikipedia articles, extracts measurable content features, calculates a percentile-based content-richness score, identifies the lowest-scoring group of the analyzed sample, and presents the results through an interactive Streamlit dashboard.

### Core Idea

```text
Analyze → Measure → Score → Explain → Rank → Explore
```

### WikiWeak Article Finder

```text
Find relatively limited-content articles
              ↓
Using measurable structured-data factors
              ↓
With transparent scoring
              ↓
Showing the actual factors behind the score
              ↓
Through an interactive dashboard
```

---

# ⭐ Project Status

**Completed Prototype**

The project includes:

- Dataset analysis
- Feature extraction
- Word-count-based content analysis
- Content-richness scoring
- Article ranking
- Limited-content detection
- Results CSV
- Interactive Streamlit dashboard
- Search and filtering
- Article score inspection
- Score explanation
- CSV export
- Complete project documentation
