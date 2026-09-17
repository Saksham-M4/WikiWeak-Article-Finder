# 📚 WikiWeak Article Finder

A data-driven tool for identifying Wikipedia articles with relatively low content-richness scores.

## 🎯 Project Overview

WikiWeak Article Finder analyzes a sample of Wikipedia articles from Wikimedia's Wikipedia Structured Contents dataset.

The system extracts measurable content factors, converts them into percentile ranks, applies weighted scoring, and ranks articles according to their relative content richness.

The project is designed to help identify articles that have relatively limited measurable content within the analyzed sample.

## 🔄 Project Workflow

Wikipedia Structured Contents Dataset
        ↓
Select 10,000-article sample
        ↓
Extract article features
        ↓
Calculate percentile ranks
        ↓
Apply weighted scoring
        ↓
Calculate Content-Richness Score
        ↓
Rank articles
        ↓
Identify bottom 5%
        ↓
Interactive Streamlit Dashboard

## 📊 Factors Used

| Factor | Weight | What it measures |
|---|---:|---|
| Article Length | 40% | Amount of article content |
| Section Count | 20% | Article structure |
| References | 20% | Available references |
| Infobox Fields | 10% | Structured information |
| Images | 10% | Available visual content |

## 🧮 Scoring Method

Each factor is converted into a percentile rank within the analyzed sample.

The final score is calculated as:

Content-Richness Score =
(Article Length Percentile × 0.40)
+ (Section Count Percentile × 0.20)
+ (Infobox Fields Percentile × 0.10)
+ (Images Percentile × 0.10)
+ (References Percentile × 0.20)

The weighted score is multiplied by 100 to produce a score from approximately 0–100.

## 📈 Results

The current analysis contains:

- **10,000 articles analyzed**
- **502 articles identified in the bottom 5%**
- **11.76** content-richness score threshold

The dashboard allows users to search articles, filter by score, inspect individual article factors, visualize score distributions, and export filtered results.

## 🖥️ Dashboard Features

- 🔎 Article search
- 🎚️ Content-richness score filtering
- 📋 Ranked article results
- 📈 Score distribution visualization
- 📉 Lowest-score article visualization
- 🔍 Individual article score breakdown
- 🔗 Direct Wikipedia article links
- 📥 CSV export
- 🧮 Transparent scoring methodology

## 🛠️ Technologies Used

- Python
- Pandas
- Polars
- Streamlit
- Matplotlib
- Jupyter Notebook
- Kaggle
- Wikimedia Wikipedia Structured Contents dataset

## 🚀 How to Run

Clone the repository:

```bash
git clone https://github.com/Saksham-M4/WikiWeak-Article-Finder.git
cd WikiWeak-Article-Finder
pip install streamlit pandas matplotlib
streamlit run app.py
